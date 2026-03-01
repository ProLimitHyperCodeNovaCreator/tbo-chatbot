'use client';

import React from 'react';
import { Send, Paperclip, Mic, Square } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ChatMessage, HotelOption, TransportOption } from '@/lib/types';
import HotelOptions from './HotelOptions';
import TransportOptions from './TransportOptions';

interface ChatAreaProps {
  messages: ChatMessage[];
  onSendMessage?: (message: string) => void;
  onToggleVoice?: () => void;
  placeholder?: string;
  hotels?: HotelOption[];
  selectedHotelId?: string;
  onSelectHotel?: (hotelId: string) => void;
  transportOptions?: TransportOption[];
  selectedTransportId?: string;
  onSelectTransport?: (transportId: string) => void;
  isLoading?: boolean;
  isRecording?: boolean;
}

export default function ChatArea({
  messages,
  onSendMessage,
  onToggleVoice,
  placeholder = "What would you like to explore next?",
  hotels,
  selectedHotelId,
  onSelectHotel,
  transportOptions,
  selectedTransportId,
  onSelectTransport,
  isLoading = false,
  isRecording = false,
}: ChatAreaProps) {
  const [input, setInput] = React.useState('');
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage?.(input);
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-6 space-y-6 bg-white scrollbar-hidden">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {message.sender === 'agent' && message.avatar && (
              <img
                src={message.avatar}
                alt={message.name}
                className="w-10 h-10 rounded-full object-cover shrink-0"
              />
            )}
            <div
              className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-2xl ${message.sender === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-white text-gray-900 border border-gray-200 rounded-bl-none'
                }`}
            >
              <p className="text-sm leading-relaxed">{message.message}</p>
              
              {/* Agent Activity Indicator */}
              {message.isLoading && (
                <div className="mt-4 pt-3 border-t border-gray-300 space-y-2">
                  {/* Current Activity */}
                  {message.currentActivity && (
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
                      <span className="inline-block w-4 h-4">
                        {message.currentActivity.startsWith('✅') ? (
                          '✅'
                        ) : message.currentActivity.startsWith('❌') ? (
                          '❌'
                        ) : (
                          <svg className="animate-spin h-4 w-4 text-orange-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                        )}
                      </span>
                      {message.currentActivity}
                    </div>
                  )}
                  
                  {/* All Activities */}
                  {message.agentActivity && message.agentActivity.length > 0 && (
                    <div className="space-y-1">
                      {message.agentActivity.map((activity, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-xs text-gray-600">
                          <span className="text-gray-400">•</span>
                          {activity}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Hotel Options in Chat */}
        {hotels && hotels.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="bg-white rounded-lg p-4 lg:p-6">
              <HotelOptions
                title="Top Hotel Options"
                hotels={hotels}
                selectedHotelId={selectedHotelId}
                onSelectHotel={onSelectHotel}
                gridCols="grid-cols-1 sm:grid-cols-2"
              />
            </div>
          </div>
        )}

        {/* Transport Options in Chat */}
        {transportOptions && transportOptions.length > 0 && (
          <div className="mt-4">
            <div className="bg-white rounded-lg p-4 lg:p-6">
              <TransportOptions
                title="Best Transport Options"
                options={transportOptions}
                selectedTransportId={selectedTransportId}
                onSelectTransport={onSelectTransport}
              />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4 lg:p-6">
        <div className="flex gap-2 items-center">
          <div className="flex-1 flex items-center bg-gray-100 rounded-full px-4 py-2 gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder={isRecording ? 'Listening...' : placeholder}
              disabled={isLoading || isRecording}
              className="flex-1 bg-transparent outline-none text-sm text-gray-900 placeholder-gray-600 disabled:opacity-50"
            />
            <button
              onClick={onToggleVoice}
              disabled={isLoading}
              className={`p-2 rounded-full transition-colors ${
                isRecording
                  ? 'bg-red-500 text-white hover:bg-red-600'
                  : 'hover:bg-gray-200 text-gray-600'
              }`}
              aria-label={isRecording ? 'Stop recording' : 'Start recording'}
            >
              {isRecording ? <Square size={18} fill="currentColor" /> : <Mic size={18} />}
            </button>
            <button className="p-2 hover:bg-gray-200 rounded-full transition-colors">
              <Paperclip size={18} className="text-gray-600" />
            </button>
          </div>
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isLoading || isRecording}
            className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-3 h-full flex items-center justify-center transition-colors disabled:opacity-50"
          >
            <Send size={18} />
          </Button>
        </div>
      </div>
    </div>
  );
}
