import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "Fetch current URL-bearing top stories from the public Hacker News API.",
  args: {
    limit: tool.schema.number().int().min(1).max(50).optional().describe("Optional number of ranked stories to return; defaults to 10"),
  },
  async execute(args, context) {
    // Resolve the paired script from this tool file, not from the Git worktree.
    // OpenCode can report a parent directory as context.worktree in nested repos.
    const script = path.join(import.meta.dir, "fetch_hn.py")
    const limit = args.limit ?? 10
    const result = await Bun.$`python3 ${script} ${limit}`.text()
    return result.trim()
  },
})
