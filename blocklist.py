"""
blocklist.py

This file contains the blocklist of JWT tokens. It will be imported by app and logout resource 
so that tokens can be added to the blocklist when user logs out
"""

BLOCKLIST = set()