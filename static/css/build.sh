#!/bin/bash
CURRENT_DIR=$(pwd)
cd "$CURRENT_DIR"
echo "Rebuilding stylesheet..."
/usr/bin/lessc less/root.less styles.css