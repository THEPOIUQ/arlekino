#!/usr/bin/env python3
"""Shadow C2 Quick Start - Complete System Launch.

Automated deployment and testing script.
"""

import argparse
import signal
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


class QuickStart:
    """Helper responsible for orchestrating the local Shadow C2 demo."""

    def __init__(self, output_dir="/mnt/okcomputer/output", port=8080, open_browser=True):
        self.output_dir = Path(output_dir).expanduser()
        self.port = port
        self.open_browser = open_browser
        self.server_process = None
        self.beacon_process = None
        self.running = True

    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n[!] Shutting down Shadow C2 system...")
        self.cleanup()
        sys.exit(0)

    def print_banner(self):
        """Print startup banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SHADOW C2 QUICK START                                ║
║                    Complete System Deployment                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def check_system(self):
        """Check system readiness."""
        print("[+] Checking system readiness...")

        if not (sys.version_info.major >= 3 and sys.version_info.minor >= 7):
            print("[!] Python 3.7+ required")
            return False

        if not self.output_dir.exists():
            print(f"[!] Output directory does not exist: {self.output_dir}")
            return False

        required_files = [
            "server/simple_server.py",
            "advanced_stager",
            "start_c2.sh",
        ]

        missing_files = [file for file in required_files if not (self.output_dir / file).exists()]
        if missing_files:
            for file in missing_files:
                print(f"[!] Required file not found: {file}")
            return False

        print("[✓] System ready for deployment")
        return True

    def start_server(self):
        """Start C2 server."""
        print("[+] Starting C2 server...")

        try:
            self.server_process = subprocess.Popen(
                [
                    sys.executable,
                    "server/simple_server.py",
                    "--port",
                    str(self.port),
                ],
                cwd=self.output_dir,
            )

            time.sleep(3)

            if self.server_process.poll() is None:
                print(f"[✓] C2 server started (PID: {self.server_process.pid})")
                return True

            print("[!] Server failed to start")
            return False

        except Exception as exc:  # pragma: no cover - defensive logging for runtime failures
            print(f"[!] Error starting server: {exc}")
            return False

    def start_beacon(self):
        """Start beacon in background."""
        print("[+] Starting beacon...")

        try:
            beacon_path = self.output_dir / "advanced_stager"
            beacon_path.chmod(0o755)

            self.beacon_process = subprocess.Popen(["./advanced_stager"], cwd=self.output_dir)
            print(f"[✓] Beacon started (PID: {self.beacon_process.pid})")
            return True

        except FileNotFoundError:
            print("[!] Beacon executable not found after initial checks")
            return False
        except Exception as exc:  # pragma: no cover - defensive logging for runtime failures
            print(f"[!] Error starting beacon: {exc}")
            return False

    def open_dashboard(self):
        """Open web dashboard."""
        if not self.open_browser:
            print(
                "[i] Dashboard auto-open disabled. Visit "
                f"http://localhost:{self.port}/dashboard manually."
            )
            return

        print("[+] Opening dashboard...")
        time.sleep(2)
        webbrowser.open(f"http://localhost:{self.port}/dashboard")
        print("[✓] Dashboard opened in browser")

    def monitor_system(self):
        """Monitor system status."""
        print("\n" + "=" * 60)
        print("SYSTEM MONITORING")
        print("=" * 60)

        try:
            while self.running:
                if self.server_process and self.server_process.poll() is not None:
                    print("\n[!] Server process died")
                    break

                if self.beacon_process and self.beacon_process.poll() is not None:
                    print("\n[!] Beacon process died")

                print(f"[+] System running on port {self.port} - {time.strftime('%H:%M:%S')}", end="\r")
                time.sleep(10)
        except KeyboardInterrupt:
            pass
        finally:
            print("\n")

    def cleanup(self):
        """Clean up processes."""
        self.running = False
        print("\n[+] Cleaning up...")

        if self.server_process and self.server_process.poll() is None:
            print("[+] Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()

        if self.beacon_process and self.beacon_process.poll() is None:
            print("[+] Stopping beacon...")
            self.beacon_process.terminate()
            self.beacon_process.wait()

        print("[✓] Cleanup completed")

    def run(self):
        """Run complete quick start."""
        signal.signal(signal.SIGINT, self.signal_handler)

        self.print_banner()

        if not self.check_system():
            return False

        if not self.start_server():
            self.cleanup()
            return False

        if not self.start_beacon():
            print("[!] Warning: Beacon failed to start")

        self.open_dashboard()

        print("\n" + "=" * 60)
        print("SHADOW C2 SYSTEM DEPLOYED SUCCESSFULLY!")
        print("=" * 60)
        print("")
        print("🎯 What you can do now:")
        print("   • View beacons in the dashboard")
        print("   • Send commands to connected beacons")
        print("   • Monitor system activity")
        print("   • Access all C2 features")
        print("")
        print(f"🌐 Dashboard: http://localhost:{self.port}/dashboard")
        print(f"📡 Beacons: http://localhost:{self.port}/beacons")
        print("")
        print("⚡ Press Ctrl+C to shut down the system")
        print("")

        try:
            self.monitor_system()
        finally:
            self.cleanup()

        return True


def parse_args():
    """Parse CLI arguments for the quick start helper."""

    parser = argparse.ArgumentParser(description="Shadow C2 quick start helper")
    parser.add_argument(
        "--output-dir",
        default="/mnt/okcomputer/output",
        help="Path to the Shadow C2 build output (default: /mnt/okcomputer/output)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for the local admin server (default: 8080)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not automatically open the dashboard in the system browser",
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    quick_start = QuickStart(
        output_dir=args.output_dir,
        port=args.port,
        open_browser=not args.no_browser,
    )

    try:
        success = quick_start.run()

        if success:
            print("\n" + "=" * 60)
            print("✅ SHADOW C2 DEPLOYMENT COMPLETED SUCCESSFULLY!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ DEPLOYMENT FAILED")
            print("=" * 60)

    except Exception as exc:  # pragma: no cover - defensive logging for runtime failures
        print(f"\n[!] Unexpected error: {exc}")
        quick_start.cleanup()


if __name__ == '__main__':
    main()
