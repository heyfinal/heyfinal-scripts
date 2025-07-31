#!/bin/bash
# Claude Code Startup Hook
# This should be executed automatically when Claude Code starts a new session

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'  
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Claude Code Session Initializing...${NC}"

# Check if CLAUDE.md exists and display key instructions
if [ -f "/home/kali/.claude/CLAUDE.md" ]; then
    echo -e "${GREEN}✅ Loading CLAUDE.md configuration...${NC}"
    
    # Extract and display critical instructions
    echo -e "${YELLOW}📋 Active Configuration:${NC}"
    echo "• Root: /mnt/mycloud-kali (knowledge base, research, projects)" 
    echo "• GitHub: sync to user heyfinal"
    echo "• Sudo password: werds"
    echo "• Check knowledge base before API calls"
    echo "• Run /compact before saving memory"
    echo "• Never use placeholder/mock code"
    echo "• Autonomous operation (minimal approval requests)"
    
    # Run Python auto-init if available
    if [ -f "/home/kali/.claude/auto-init.py" ]; then
        python3 /home/kali/.claude/auto-init.py > /tmp/claude-init.log 2>&1
    fi
    
else
    echo -e "${RED}⚠️  CLAUDE.md not found - creating default${NC}"
    
    # Create default CLAUDE.md if missing
    cat > /home/kali/.claude/CLAUDE.md << 'EOF'
# System Configuration
Root: `/mnt/mycloud-kali` with folders: knowledge base, research, ai convos, code warehouse, project backups, current active projects, completed projects
GitHub: sync all production files to user `heyfinal`
Sudo password: `werds`

# Workflow
- Check knowledge base/research folders before API calls to minimize costs
- Run `/compact` before saving conversations/memory/research
- Backup projects before builds (maintain 1 backup per project)
- Move completed projects: current active → completed
- Store all scripts in code warehouse
- Code everything needed (dependencies, folder structure, permissions)
- Stay current with modern tech (Python/Swift/Xcode)

# Code Standards
- Never use placeholder/mock/demo code
- Minimize user input requirements  
- No decorative borders around macros
- Production-ready code only
- Spell check all instructions

# Project Management
- Create/reference README.md during long conversations to maintain scope
- Autonomous operation (minimal approval requests)
- Discretely backup projects before builds to prevent data loss
EOF

    echo -e "${GREEN}✅ Created default CLAUDE.md${NC}"
fi

echo -e "${BLUE}🎯 Claude Code ready with configuration loaded${NC}"