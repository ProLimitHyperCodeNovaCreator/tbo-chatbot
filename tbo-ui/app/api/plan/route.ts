// app/api/plan/route.ts
import { NextResponse } from "next/server";

export async function POST(req: Request) {
    try {
        const body = await req.json();

        const orchestratorUrl = process.env.ORCHESTRATOR_URL || "http://localhost:8000";

        const orchestratorResponse = await fetch(`${orchestratorUrl}/recommend/travel-plan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!orchestratorResponse.ok) {
            throw new Error(`Orchestrator returned ${orchestratorResponse.status}`);
        }

        const data = await orchestratorResponse.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error("Orchestrator API Error:", error);
        return NextResponse.json(
            { error: "Failed to connect to Orchestrator Agent" },
            { status: 500 }
        );
    }
}
