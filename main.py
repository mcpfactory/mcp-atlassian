# Entry Point for mcp server in mcp_factory

import asyncio
from mcp_factory.server import main
import handler

if __name__ == "__main__":
    asyncio.run(main())