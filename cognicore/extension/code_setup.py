import os
import subprocess
import sys
import logging
logger = logging.getLogger("cognicore.extension.code_setup")


def main():
    logger.info("Setting up CogniCore Memory for Claude Code...")
    logger.info("This will add the 'cognicore-memory' MCP server to your Claude Code configuration.")
    logger.info("Make sure you have Claude Code installed (`npm install -g @anthropic-ai/claude-code`).\n")

    # We want to run: claude mcp add cognicore-memory uvx cognicore-env[extension] cognicore-extension
    # Or since we are installing it in the current env, we could use the current uvx if available,
    # but the simplest robust way is exactly what the user requested for one-command integration.

    cmd = [
        "claude",
        "mcp",
        "add",
        "cognicore-memory",
        "uvx",
        "cognicore-env[extension]",
        "cognicore-extension"
    ]

    try:
        # We use shell=True on Windows if `claude` is a cmd/ps1 script from npm
        is_win = sys.platform.startswith("win")
        result = subprocess.run(cmd, check=True, shell=is_win)  # nosec B602

        logger.info("\n✅ Success! CogniCore Memory is now integrated with Claude Code.")
        logger.info("When you run `claude`, it will have access to persistent global and project-scoped memory.")
        logger.info("Try asking it to remember a project fact, then start a new session to see it recalled!")

    except subprocess.CalledProcessError as e:
        logger.info(f"\n❌ Failed to add MCP server. Claude Code CLI might not be installed or configured correctly.")
        logger.info(f"Error details: {e}")
        logger.info("\nYou can try adding it manually by running:")
        logger.info(" ".join(cmd))
        sys.exit(1)
    except FileNotFoundError:
        logger.info("\n❌ Could not find the 'claude' command.")
        logger.info("Please ensure Claude Code is installed and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()
