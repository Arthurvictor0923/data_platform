# 烛龙大数据平台 · 数据模型与配置管理优化

武汉柯灿 × 北大荒「烛龙大数据平台」数据模型仓库，托管**系统管理 → 目录配置**模块的**目录元数据接口发布交互原型**，以及平台各业务线界面截图。

在线访问：**<https://arthurvictor0923.github.io/data_platform/>**

---

## 目录结构

```
.
├── 配置管理目录功能优化/
│   └── 目录配置-元数据接口发布.html     # 交互原型（自包含单文件，CSS/JS 全内联，无外部依赖）
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
start "配置管理目录功能优化\目录配置-元数据接口发布.html"

# macOS / Linux
open "配置管理目录功能优化/目录配置-元数据接口发布.html"
```

> 站点首页会自动取 `配置管理目录功能优化/` 下**最近修改**的 `.html`，
> 换原型或改文件名都不必改脚本；若目录里同时留了多个 HTML，请把旧的删掉以免误取。

如需连同业务截图画廊一起预览，执行站点组装脚本：

```bash
python publish/build_site.py --out _site
# 然后访问 _site/index.html 与 _site/screenshots/index.html
```

## 发布到 GitHub Pages

仓库当前已配置为 **GitHub Actions 自动发布**（Pages Source = GitHub Actions），
**推送 `main` 即自动上线**，无需任何手工操作。

推送后约 1–2 分钟完成组装与部署，可在此查看运行记录：
<https://github.com/Arthurvictor0923/data_platform/actions>

### 工作流程做了什么

`.github/workflows/pages.yml` 每次触发时依次执行：

1. 检出代码 → 2. 运行 `publish/build_site.py` 组装站点 → 3. 配置 Pages →
4. 上传站点产物 → 5. 发布到 GitHub Pages → 6. 同步 `gh-pages` 备用分支

第 6 步会持续把 `gh-pages` 分支更新为与线上一致的站点快照，
万一日后关闭 Actions，可在 Settings → Pages 把 Source 切回「Deploy from a branch → gh-pages / (root)」继续托管。

### 日常更新

```bash
# 改完原型后
git add -A && git commit -m "说明" && git push origin main
# 等 1–2 分钟后刷新 https://arthurvictor0923.github.io/data_platform/ 即可看到新版本
```

### 站点结构

| 线上路径 | 内容 |
| --- | --- |
| `/` | 目录元数据接口发布交互原型（首页） |
| `/screenshots/` | 平台 13 张业务截图画廊 |

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
