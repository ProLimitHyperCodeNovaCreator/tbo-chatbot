// app/api/chat/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const { message } = await req.json();

    // Route to the Orchestrator Agent
    const orchestratorUrl = process.env.ORCHESTRATOR_URL || "http://localhost:8000";
    
    const orchestratorResponse = await fetch(`${orchestratorUrl}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: message })
    });

    if (!orchestratorResponse.ok) {
      throw new Error(`Orchestrator returned ${orchestratorResponse.status}`);
    }

    const data = await orchestratorResponse.json();

    // The orchestrator returns { response: "text" }
    return NextResponse.json({ text: data.response });
  } catch (error) {
    console.error("Orchestrator API Error:", error);
    return NextResponse.json(
      { error: "Failed to connect to Orchestrator Agent" },
      { status: 500 }
    );
  }
}