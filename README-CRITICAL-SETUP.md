# CRITICAL: Claude Code Memory/Configuration Setup

## The Problem
Claude Code doesn't automatically read CLAUDE.md on session start, causing it to:
- Ignore user workflow preferences
- Not follow established patterns 
- Waste API calls on redundant research
- Ask for approvals when configured for autonomous operation

## The Solution
Multiple approaches to ensure Claude Code loads configuration on startup:

### 1. Manual Initialization (Immediate Fix)
**User must run this at start of each session:**
```bash
python3 /home/kali/.claude/auto-init.py
```

### 2. Shell Integration (Recommended)
Add to `.zshrc` or `.bashrc`:
```bash
# Auto-load Claude configuration when in Claude directory
if [[ "$PWD" == *"claude"* ]] || [[ -f ".claude/CLAUDE.md" ]]; then
    if [[ -f "/home/kali/.claude/auto-init.py" ]]; then
        python3 /home/kali/.claude/auto-init.py
    fi
fi
```

### 3. Environment Variable Approach
Set in shell profile:
```bash
export CLAUDE_CONFIG_LOADED="$(python3 /home/kali/.claude/auto-init.py)"
```

### 4. Hook Integration (If Supported)
If Claude Code supports startup hooks, add to configuration:
```json
{
  "startup_commands": [
    "python3 /home/kali/.claude/auto-init.py"
  ]
}
```

### 5. Alias Method
Add to shell profile:
```bash
alias claude-start="python3 /home/kali/.claude/auto-init.py && echo 'Claude Config Loaded'"
```

## Files Created

### `/home/kali/.claude/auto-init.py`
- Finds and reads all CLAUDE.md files
- Parses configuration and workflow rules
- Displays active settings for session
- Caches configuration for reference

### `/home/kali/.claude/startup-hook.sh`  
- Bash script for shell integration
- Quick configuration loading
- Fallback CLAUDE.md creation

### `/home/kali/.claude/session-config.json`
- Cached configuration from last session
- JSON format for programmatic access
- Tracks what configs were loaded

## Critical CLAUDE.md Content

The following MUST be read on every session:

```markdown
# System Configuration  
Root: `/mnt/mycloud-kali` with folders: knowledge base, research, ai convos, code warehouse, project backups, current active projects, completed projects
GitHub: sync all production files to user `heyfinal`
Sudo password: `werds`

# Workflow
- Check knowledge base/research folders before API calls to minimize costs
- Run `/compact` before saving conversations/memory/research
- Backup projects before builds (maintain 1 backup per project)
- Never use placeholder/mock/demo code
- Autonomous operation (minimal approval requests)
```

## Verification

To verify configuration is loaded:
```bash
# Check if session config exists
cat /home/kali/.claude/session-config.json

# View loaded configuration
python3 -c "
import json
with open('/home/kali/.claude/session-config.json') as f:
    config = json.load(f)
    print('Configs loaded:', config['configs_loaded'])
    print('Session start:', config['session_start'])
"
```

## User Action Required

**IMMEDIATE:** User must either:
1. Run `python3 /home/kali/.claude/auto-init.py` at start of each Claude session
2. Add the shell integration to their profile
3. Use the alias method for easy activation

**LONG-TERM:** Request Claude Code feature to support:
- Automatic CLAUDE.md reading on session start
- Built-in configuration management
- Session persistence of user preferences

## Impact of Not Loading Configuration

Without loading CLAUDE.md, Claude Code will:
- ❌ Not follow the established workflow patterns
- ❌ Ask for unnecessary approvals (violates autonomous operation rule)
- ❌ Not check knowledge base before API calls (wastes money)
- ❌ Not use proper folder structure (/mnt/mycloud-kali)
- ❌ Not sync to GitHub user heyfinal
- ❌ May use placeholder/demo code (violates production rule)

## Testing the Fix

After implementing any solution, test by starting a new Claude session and verifying:
1. Configuration loaded message appears
2. Claude knows the sudo password is "werds"
3. Claude references /mnt/mycloud-kali structure
4. Claude operates autonomously without excessive approval requests
5. Claude checks knowledge base before research

---

**This is CRITICAL for proper Claude Code operation with user preferences.**