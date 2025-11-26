import ChatInput from '@/components/chat/ChatInput';
import ChatStream from '@/components/chat/ChatStream';
export default function ChatPage(){
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Chat</h1>
      <div className="border rounded p-4 mb-4 bg-ne-card">
        <ChatStream />
      </div>
      <ChatInput />
      <div className="mt-4 text-xs text-muted-foreground">NeuroEdge can make mistakes — verify important info.</div>
    </div>
  )
}
