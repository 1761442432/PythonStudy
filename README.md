
导出依赖：
python -m pip freeze > requirements.txt
安装依赖：
python -m pip install -r requirements.txt


安装包到全局环境（创建虚拟环境后，默认安装到虚拟环境）：
pip install requests beautifulsoup4 lxml

安装包到虚拟环境（虚拟环境，仅对当前项目生效，在 .venv 目录下）：
python -m pip install requests beautifulsoup4 lxml

验证安装包安装到了哪里：
python -m pip show requests

验证安装包安装位置：
import site
print(site.getsitepackages())      # 全局 site-packages
print(site.getusersitepackages())  # 用户级 site-packages

创建虚拟环境：
python -m venv .venv

激活虚拟环境（激活后，直接用 pip install 等命令，都是指向虚拟环境）：
macOS / Linux ：        source .venv/bin/activate
Windows（CMD）：        .venv\Scripts\activate
Windows（PowerShell）： .venv\Scripts\Activate.ps1

删除虚拟环境：
直接删除 .venv 目录
