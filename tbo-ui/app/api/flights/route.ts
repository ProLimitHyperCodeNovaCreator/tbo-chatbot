// app/api/flights/route.ts
// Proxy to the transport-search-api (port 8001) — returns FlightOption[] for the UI
import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { origin, destination, date, adults = 1 } = body;

    if (!origin || !destination || !date) {
      return NextResponse.json(
        { error: "origin, destination, and date are required" },
        { status: 400 }
      );
    }

    const transportUrl =
      process.env.TRANSPORT_API_URL || "http://localhost:8001";

    const transportResponse = await fetch(
      `${transportUrl}/api/search-transport`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ origin, destination, date, adults }),
      }
    );

    if (!transportResponse.ok) {
      const text = await transportResponse.text();
      console.error("Transport API error:", transportResponse.status, text);
      return NextResponse.json(
        { error: `Transport API returned ${transportResponse.status}` },
        { status: transportResponse.status }
      );
    }

    const data = await transportResponse.json();

    // Filter to flights only and map to the UI's FlightOption shape
    const flights = (data.transport_options ?? [])
      .filter((opt: any) => opt.type === "flight")
      .map((f: any, idx: number) => ({
        id: `${f.airline_code || "FL"}-${idx}-${Date.now()}`,
        airline: f.provider || "Airline",
        airlineCode: f.airline_code ?? undefined,
        flightNumber: f.flight_number ?? undefined,
        origin: f.origin,
        destination: f.destination,
        departureTime: f.departure_time,
        arrivalTime: f.arrival_time,
        duration: f.duration,
        stops: f.stops ?? 0,
        price: f.price,
        currency: f.currency ?? "INR",
        cabinClass: f.cabin_class ?? "Economy",
      }));

    return NextResponse.json({ flights });
  } catch (error) {
    console.error("Flights API error:", error);
    return NextResponse.json(
      { error: "Failed to fetch flights from transport service" },
      { status: 500 }
    );
  }
}
