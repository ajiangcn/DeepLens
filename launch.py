#!/usr/bin/env python3
"""
DeepLens Launcher - Easy way to start DeepLens UI or CLI
"""

import sys
import argparse
from deeplens.config import DeepLensConfig


def main():
    """Main launcher entry point"""
    parser = argparse.ArgumentParser(
        description="DeepLens: Multi-agent research analysis system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Launch web UI
  python launch.py --ui
  
  # Launch interactive CLI
  python launch.py --cli
  
  # Launch web UI with custom port
  python launch.py --ui --port 8080
  
  # Share web UI publicly
  python launch.py --ui --share
        """
    )
    
    parser.add_argument(
        "--ui",
        action="store_true",
        help="Launch web UI (Gradio interface)"
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Launch interactive CLI"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port for web UI (default: 7860)"
    )
    
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public share link for web UI"
    )
    
    parser.add_argument(
        "--model",
        default=None,
        help="Model to use (default: from .env or gpt-4)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = DeepLensConfig.from_env()
    if args.model:
        config.model = args.model
    config.ui_port = args.port
    
    # Validate configuration
    if not config.use_azure and not config.api_key:
        print("❌ Error: No API credentials configured")
        print("\nFor Azure OpenAI (DefaultAzureCredential):")
        print("  Set USE_AZURE=true and AZURE_API_BASE in .env")
        print("  Make sure you're logged in via 'az login'")
        print("\nFor OpenAI:")
        print("  Set OPENAI_API_KEY in .env")
        sys.exit(1)
    
    # Launch appropriate interface
    if args.ui:
        print("🚀 Launching DeepLens Web UI...")
        from deeplens.ui import DeepLensUI
        ui = DeepLensUI(config)
        ui.launch(share=args.share, server_port=args.port)
    elif args.cli:
        print("🚀 Launching DeepLens Interactive CLI...")
        import asyncio
        from deeplens.interactive_cli import InteractiveCLI
        cli = InteractiveCLI(config)
        asyncio.run(cli.run())
    else:
        # Default: show menu
        print("\n" + "="*60)
        print("🔬 DeepLens: Multi-Agent Research Analysis System")
        print("="*60)
        print("\nChoose an interface:")
        print("  1. Web UI (Gradio) - Recommended for most users")
        print("  2. Interactive CLI (Terminal)")
        print("  3. Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            from deeplens.ui import DeepLensUI
            ui = DeepLensUI(config)
            ui.launch(share=False, server_port=args.port)
        elif choice == "2":
            import asyncio
            from deeplens.interactive_cli import InteractiveCLI
            cli = InteractiveCLI(config)
            asyncio.run(cli.run())
        elif choice == "3":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print(f"❌ Invalid choice: {choice}")
            print("Please enter 1, 2, or 3")
            sys.exit(1)


if __name__ == "__main__":
    main()
