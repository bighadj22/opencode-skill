import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Scrape article pages listed in a Hacker News scout JSON handoff using requests and BeautifulSoup.",
  args: {
    inputPath: tool.schema.string().describe("Path to the scout JSON handoff relative to the project root"),
  },
  async execute(args, context) {
    // Resolve the paired script from this tool file, not from the Git worktree.
    const projectRoot = path.resolve(import.meta.dir, "../..")
    const script = path.join(import.meta.dir, "scrape_articles.py")
    const inputPath = path.isAbsolute(args.inputPath)
      ? args.inputPath
      : path.join(projectRoot, args.inputPath)
    const result = await Bun.$`python3 ${script} ${inputPath}`.text()
    return result.trim()
  },
})
