# 烛龙大数据平台 · 数据模型与配置管理优化

武汉柯灿 × 北大荒「烛龙大数据平台」数据模型仓库，托管**系统管理 → 目录配置**模块的**资产复制交互原型**，以及平台各业务线界面截图。

在线访问：**<https://arthurvictor0923.github.io/data_platform/>**

---

## 目录结构

```
.
├── 配置管理目录功能优化/
│   └── 目录配置-资产复制交互原型.html   # 交互原型（自包含单文件，CSS/JS 全内联，无外部依赖）
├── 平台业务截图/                        # 平台现有业务界面截图（13 张）
├── publish/
│   └── build_site.py                   # 站点组装脚本：原型 → index.html，截图 → 画廊页
├── .github/workflows/pages.yml          # GitHub Actions 自动发布工作流
└── .gitignore
```

## 本地预览

原型是单文件自包含 HTML，双击直接用浏览器打开即可，无需构建、无需起服务：

```bash
# Windows
start "配置管理目录功能优化\目录配置-资产复制交互原型.html"

# macOS / Linux
open "配置管理目录功能优化/目录配置-资产复制交互原型.html"
```

如需连同业务截图画廊一起预览，执行站点组装脚本：

```bash
python publish/build_site.py --out _site
# 然后访问 _site/index.html 与 _site/screenshots/index.html
```

## 发布到 GitHub Pages

仓库采用**双通道**发布，任选其一即可：

### 通道 A · GitHub Actions（推荐，推送即自动发布）

1. 仓库 → **Settings** → **Pages**
2. **Build and deployment** → Source 选 **GitHub Actions** → Save
3. 之后每次 `git push origin main`，工作流会自动组装站点并发布

### 通道 B · gh-pages 分支

1. 仓库 → **Settings** → **Pages**
2. **Build and deployment** → Source 选 **Deploy from a branch**
3. Branch 选 **gh-pages**，目录选 **/ (root)** → Save
4. 该分支已预置组装好的站点内容；本地改动后用下面命令刷新：

```bash
python publish/build_site.py --out _site
# 将 _site 内容同步到 gh-pages 分支后推送
```

## 常用命令

```bash
git status                     # 查看改动
git add -A && git commit -m "说明"
git push origin main           # 推送到 main（触发自动发布）
```

## 注意事项

- 原型 HTML 中的**中文目录名与文件名**在 Linux 环境下大小写敏感，请勿在提交时重命名 `配置管理目录功能优化/` 与 `平台业务截图/`。
- `平台业务截图/` 中 PNG 均为业务界面真实截图，仅用于内部评审，请勿外传。
- 本仓库仅存放原型与参考资料，平台真实源码在独立的开发仓库中。
