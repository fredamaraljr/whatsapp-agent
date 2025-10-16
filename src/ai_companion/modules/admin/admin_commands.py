"""
Admin Tools Module
Provides administrative functions for system management via WhatsApp.
"""
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from ai_companion.settings import settings
from ai_companion.modules.user_management import UserManager

logger = logging.getLogger(__name__)


class AdminCommands:
    """Handles administrative commands from the admin user."""
    
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager
        self.custom_prompts = {}
        self.system_config = {}
        
    def parse_command(self, message: str) -> tuple[str, Optional[dict]]:
        """Parse admin command from message."""
        message = message.strip()
        
        # Command patterns
        if message.lower().startswith("/stats"):
            return ("stats", None)
        
        if message.lower().startswith("/users"):
            return ("users", None)
        
        if message.lower().startswith("/setprompt"):
            # Format: /setprompt GROUP\n[prompt text]
            parts = message.split("\n", 1)
            if len(parts) == 2:
                group = parts[0].replace("/setprompt", "").strip().lower()
                prompt = parts[1].strip()
                return ("setprompt", {"group": group, "prompt": prompt})
        
        if message.lower().startswith("/getprompt"):
            group = message.replace("/getprompt", "").strip().lower()
            return ("getprompt", {"group": group})
        
        if message.lower().startswith("/help"):
            return ("help", None)
        
        if message.lower().startswith("/config"):
            # Format: /config KEY=VALUE
            parts = message.replace("/config", "").strip().split("=", 1)
            if len(parts) == 2:
                key, value = parts
                return ("config", {"key": key.strip(), "value": value.strip()})
        
        if message.lower().startswith("/getconfig"):
            key = message.replace("/getconfig", "").strip()
            return ("getconfig", {"key": key})
        
        return ("unknown", None)
    
    def execute_command(self, command: str, params: Optional[dict]) -> str:
        """Execute an admin command and return the response."""
        try:
            if command == "stats":
                return self._get_stats()
            
            elif command == "users":
                return self._list_users()
            
            elif command == "setprompt":
                return self._set_prompt(params["group"], params["prompt"])
            
            elif command == "getprompt":
                return self._get_prompt(params["group"])
            
            elif command == "config":
                return self._set_config(params["key"], params["value"])
            
            elif command == "getconfig":
                return self._get_config(params["key"])
            
            elif command == "help":
                return self._get_help()
            
            else:
                return self._get_help()
                
        except Exception as e:
            logger.error(f"Error executing admin command '{command}': {e}")
            return f"❌ Erro ao executar comando: {str(e)}"
    
    def _get_stats(self) -> str:
        """Get system statistics."""
        stats = self.user_manager.get_user_stats()
        
        response = "📊 **Estatísticas do Sistema**\n\n"
        response += f"👥 Total de usuários: {stats.get('total_users', 0)}\n"
        response += f"💬 Total de mensagens: {stats.get('total_messages', 0)}\n"
        response += f"🕐 Interações (24h): {stats.get('recent_interactions_24h', 0)}\n\n"
        
        response += "**Usuários por grupo:**\n"
        for group, count in stats.get('users_by_group', {}).items():
            response += f"  • {group}: {count}\n"
        
        return response
    
    def _list_users(self) -> str:
        """List all users with details."""
        # This would query the database for all users
        # For now, returning a placeholder
        return "👥 Lista de usuários:\n\nUse /stats para ver estatísticas gerais."
    
    def _set_prompt(self, group: str, prompt: str) -> str:
        """Set custom prompt for a group."""
        valid_groups = ["admin", "monitori", "fps", "avila", "ffl"]
        
        if group not in valid_groups:
            return f"❌ Grupo inválido. Grupos válidos: {', '.join(valid_groups)}"
        
        self.custom_prompts[group] = {
            "prompt": prompt,
            "updated_at": datetime.now().isoformat(),
            "updated_by": "admin"
        }
        
        # Save to file
        try:
            with open("/app/data/custom_prompts.json", "w") as f:
                json.dump(self.custom_prompts, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving custom prompt: {e}")
        
        return f"✅ Prompt atualizado para o grupo '{group}'"
    
    def _get_prompt(self, group: str) -> str:
        """Get current prompt for a group."""
        if group in self.custom_prompts:
            prompt_data = self.custom_prompts[group]
            return f"📝 **Prompt do grupo '{group}':**\n\n{prompt_data['prompt']}\n\n_Atualizado em: {prompt_data['updated_at']}_"
        else:
            return f"ℹ️ Nenhum prompt customizado definido para o grupo '{group}'"
    
    def _set_config(self, key: str, value: str) -> str:
        """Set a configuration value."""
        self.system_config[key] = value
        
        # Save to file
        try:
            with open("/app/data/system_config.json", "w") as f:
                json.dump(self.system_config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
        
        return f"✅ Configuração '{key}' definida como '{value}'"
    
    def _get_config(self, key: str) -> str:
        """Get a configuration value."""
        if key in self.system_config:
            return f"⚙️ {key} = {self.system_config[key]}"
        else:
            return f"ℹ️ Configuração '{key}' não encontrada"
    
    def _get_help(self) -> str:
        """Get help text for admin commands."""
        return """🛠️ **Comandos de Administração**

**Estatísticas:**
• `/stats` - Visualizar estatísticas do sistema
• `/users` - Listar todos os usuários

**Gerenciamento de Prompts:**
• `/setprompt GRUPO` - Definir prompt customizado para um grupo
  Exemplo:
  ```
  /setprompt monitori
  Você é um assistente especializado em análise de dados...
  ```
• `/getprompt GRUPO` - Ver prompt atual de um grupo

**Configurações:**
• `/config CHAVE=VALOR` - Definir configuração
• `/getconfig CHAVE` - Ver configuração

**Outros:**
• `/help` - Ver esta mensagem de ajuda

**Grupos disponíveis:**
admin, monitori, fps, avila, ffl"""

    def get_custom_prompt(self, group: str) -> Optional[str]:
        """Get custom prompt for a group if it exists."""
        if group in self.custom_prompts:
            return self.custom_prompts[group]["prompt"]
        return None
    
    def load_custom_prompts(self):
        """Load custom prompts from file."""
        try:
            with open("/app/data/custom_prompts.json", "r") as f:
                self.custom_prompts = json.load(f)
                logger.info(f"Loaded {len(self.custom_prompts)} custom prompts")
        except FileNotFoundError:
            logger.info("No custom prompts file found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading custom prompts: {e}")
    
    def load_system_config(self):
        """Load system configuration from file."""
        try:
            with open("/app/data/system_config.json", "r") as f:
                self.system_config = json.load(f)
                logger.info(f"Loaded {len(self.system_config)} config values")
        except FileNotFoundError:
            logger.info("No system config file found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading system config: {e}")
