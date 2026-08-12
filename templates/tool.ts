import { tool } from "@opencode-ai/plugin"
import path from "path"

export default tool({
  description: "{{TOOL_DESCRIPTION}}",
  args: {
    argName: tool.schema.string().describe("{{ARG_DESCRIPTION}}"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, ".opencode/tools/{{TOOL_NAME}}.py")
    const result = await Bun.$`python3 ${script} ${args.argName}`.text()
    return result.trim()
  },
})
