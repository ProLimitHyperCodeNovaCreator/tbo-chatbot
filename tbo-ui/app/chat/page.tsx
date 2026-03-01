'use client';

import React, { useState, useRef, useEffect } from 'react';
import Header from '@/components/Header';
import Sidebar from '@/components/Sidebar';
import ChatArea from '@/components/ChatArea';
import QuotePanel from '@/components/QuotePanel';
import {
  mockAgent,
  mockChatMessages,
  mockHotels,
  mockTransport,
  mockQuote,
  mockHistory,
  mockSavedPlans,
  mockReports,
  mockRecommendedHotels,
} from '@/lib/mockData';
import { ChatMessage } from '@/lib/types';

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>(mockChatMessages);
  const [selectedHotel, setSelectedHotel] = useState<string | undefined>();
  const [selectedTransport, setSelectedTransport] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [showQuotePanel, setShowQuotePanel] = useState(false);

  const recognitionRef = useRef<any>(null);

  // Initialize Speech Recognition on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognitionRef.current = new SpeechRecognition();
        recognitionRef.current.continuous = false;
        recognitionRef.current.interimResults = false;
        recognitionRef.current.lang = 'en-US';
      }
    }
  }, []);

  // ElevenLabs Text-to-Speech function
  const speakResponse = async (text: string) => {
    try {
      const response = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) throw new Error('Audio fetch failed');

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      audio.play();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  // Main logic to handle messaging (both text and voice)
  const processMessage = async (
    text: string,
    isVoiceInput: boolean = false,
  ) => {
    if (!text.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      message: text.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    
    // Show QuotePanel on first user interaction
    if (!showQuotePanel) {
      setShowQuotePanel(true);
    }

    // Add thinking message while processing with agent activities
    const thinkingMessageId = (Date.now() + 1).toString();
    const thinkingMessage: ChatMessage = {
      id: thinkingMessageId,
      sender: 'agent',
      avatar: mockAgent.image,
      name: mockAgent.name,
      message: 'Processing your request...',
      isLoading: true,
      agentActivity: ['🔍 Analyzing request', '🌐 Searching for options', '💭 Generating recommendations'],
      currentActivity: '🔍 Analyzing request',
    };

    setMessages((prev) => [...prev, thinkingMessage]);
    setIsLoading(true);

    // Simulate agent activity progression
    const activitySequence = [
      '🔍 Analyzing request',
      '🌐 Searching for hotels & flights',
      '💰 Comparing prices',
      '📊 Analyzing patterns',
      '🎯 Generating recommendations',
    ];

    let currentActivityIndex = 0;
    const activityInterval = setInterval(() => {
      if (currentActivityIndex < activitySequence.length - 1) {
        currentActivityIndex++;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === thinkingMessageId
              ? {
                  ...msg,
                  currentActivity: activitySequence[currentActivityIndex],
                }
              : msg
          )
        );
      }
    }, 800); // Update activity every 800ms

    try {
      // 1. Send text to Gemini API (or your AI endpoint)
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error);

      const replyText = data.text;

      clearInterval(activityInterval);

      // 2. Replace thinking message with actual response
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === thinkingMessageId
            ? {
                ...msg,
                message: replyText,
                isLoading: false,
                currentActivity: '✅ Complete',
                agentActivity: [],
              }
            : msg
        )
      );

      // 3. ONLY play the ElevenLabs audio if the user used the microphone
      if (isVoiceInput) {
        speakResponse(replyText);
      }
    } catch (error) {
      console.error('Failed to fetch response:', error);
      clearInterval(activityInterval);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === thinkingMessageId
            ? {
                ...msg,
                message: 'Sorry, I encountered an error connecting to the AI.',
                isLoading: false,
                currentActivity: '❌ Error',
                agentActivity: [],
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Triggered when user sends a text message
  const handleSendMessage = (message: string) => {
    processMessage(message, false); // false = don't speak back
  };

  // Triggered when user clicks the Microphone
  const handleToggleVoice = () => {
    if (!recognitionRef.current) {
      alert('Voice input isn\'t supported in this browser. Try Chrome or Edge.');
      return;
    }

    if (isRecording) {
      recognitionRef.current.stop();
      setIsRecording(false);
    } else {
      recognitionRef.current.onresult = (e: any) => {
        const transcript = e.results[0][0].transcript;
        if (transcript) {
          processMessage(transcript, true); // true = speak back via ElevenLabs!
        }
      };

      recognitionRef.current.onerror = (e: any) => {
        if (e.error !== 'aborted')
          console.error('Speech recognition error:', e.error);
        setIsRecording(false);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current.start();
      setIsRecording(true);
    }
  };

  const handleGeneratePDF = () => {
    alert('PDF generation feature will be implemented');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 overflow-hidden">
      {/* Header */}
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Mobile Drawer */}
        {sidebarOpen && (
          <div className="fixed inset-0 z-30 md:hidden bg-black/50" onClick={() => setSidebarOpen(false)}>
            <div onClick={(e) => e.stopPropagation()} className="h-full overflow-auto">
              <Sidebar
                history={mockHistory}
                savedPlans={mockSavedPlans}
                reports={mockReports}
                agent={mockAgent}
                isOpen={sidebarOpen}
              />
            </div>
          </div>
        )}

        {/* Sidebar - Desktop */}
        <Sidebar
          history={mockHistory}
          savedPlans={mockSavedPlans}
          reports={mockReports}
          agent={mockAgent}
        />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col lg:flex-row gap-4 overflow-hidden p-4 bg-white">
          {/* Center: Chat Area */}
          <div className="flex-1 flex flex-col overflow-hidden min-w-0">
            <div className="flex-1 bg-white rounded-lg shadow flex flex-col overflow-hidden">
              <ChatArea
                messages={messages}
                onSendMessage={handleSendMessage}
                onToggleVoice={handleToggleVoice}
                hotels={mockHotels}
                selectedHotelId={selectedHotel}
                onSelectHotel={setSelectedHotel}
                transportOptions={mockTransport}
                selectedTransportId={selectedTransport}
                onSelectTransport={setSelectedTransport}
                isLoading={isLoading}
                isRecording={isRecording}
              />
            </div>
          </div>

          {/* Right: Quote Panel - Show only after user interaction */}
          {showQuotePanel && (
            <div className="w-full lg:w-72 flex-shrink-0 overflow-y-auto animate-slideInRight">
              <QuotePanel
                quote={mockQuote}
                recommendedHotels={mockRecommendedHotels}
                onGeneratePDF={handleGeneratePDF}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
