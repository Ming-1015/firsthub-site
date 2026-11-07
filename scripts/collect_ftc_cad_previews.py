"""Refresh per-link previews for both FIRSTHub libraries.

Kept as the scheduled workflow entry point; the shared collector also audits
FRC links and retires legacy single-image metadata.
"""
import asyncio
import collect_cad_previews as cad
from refresh_all_cad_previews import main

if __name__ == '__main__':
    asyncio.run(main(cad.parse_args()))
