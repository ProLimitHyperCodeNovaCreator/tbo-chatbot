'use client';

import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Search, BarChart3, Zap, Hotel, Plane, Activity, Repeat2, Shield } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4 bg-white shadow-sm">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-orange-500 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">TBO</span>
          </div>
          <span className="font-bold text-lg text-gray-800">tbo</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8">
          <a href="#" className="text-gray-600 hover:text-gray-900 text-sm font-medium">Products</a>
          <a href="#" className="text-gray-600 hover:text-gray-900 text-sm font-medium">Recent Offers</a>
          <a href="#" className="text-gray-600 hover:text-gray-900 text-sm font-medium">Contact</a>
        </div>
        
        <Button className="bg-orange-500 hover:bg-orange-600 text-white">
          Get Options
        </Button>
      </nav>

      {/* Hero Section */}
      <section className="relative px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-6 z-10">
              <div>
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-4">
                  Meet Your Intelligent Travel Agent Copilot
                </h1>
                <p className="text-lg text-gray-600">
                  AI powered assistant helping travel agents make better, faster decisions.
                </p>
              </div>
              
              <Button size="lg" className="bg-orange-500 hover:bg-orange-600 text-white w-fit">
                Get Options
              </Button>
            </div>

            {/* Right Content - Hero Image with Background */}
            <div className="relative h-80 sm:h-96 lg:h-[500px]">
              <Image
                src="/bg-hero.png"
                alt="Travel AI Copilot"
                fill
                className="object-cover rounded-xl"
                priority
              />
            </div>
          </div>
        </div>

        {/* Background wave pattern */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-blue-50 to-transparent pointer-events-none" />
      </section>

      {/* Features Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-16 sm:py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                <Search className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Live Search</h3>
              <p className="text-gray-600">
                Get real-time comprehensive search results powered by advanced algorithms.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center">
                <BarChart3 className="w-8 h-8 text-orange-500" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Smart Comparisons</h3>
              <p className="text-gray-600">
                Compare and analyze travel options instantly with intelligent insights.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                <Zap className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Multimodal Output</h3>
              <p className="text-gray-600">
                Get comprehensive presentations across all your preferred platforms.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-16 sm:py-20">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center text-gray-900 mb-16">
            One Platform For Everything Travel
          </h2>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 sm:gap-8">
            {/* Service 1 */}
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center">
                <Hotel className="w-7 h-7 text-blue-600" />
              </div>
              <p className="font-semibold text-gray-900 text-sm sm:text-base">Hotels</p>
            </div>

            {/* Service 2 */}
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="w-14 h-14 bg-orange-100 rounded-lg flex items-center justify-center">
                <Plane className="w-7 h-7 text-orange-500" />
              </div>
              <p className="font-semibold text-gray-900 text-sm sm:text-base">Flights</p>
            </div>

            {/* Service 3 */}
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center">
                <Activity className="w-7 h-7 text-blue-600" />
              </div>
              <p className="font-semibold text-gray-900 text-sm sm:text-base">Activities</p>
            </div>

            {/* Service 4 */}
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="w-14 h-14 bg-orange-100 rounded-lg flex items-center justify-center">
                <Repeat2 className="w-7 h-7 text-orange-500" />
              </div>
              <p className="font-semibold text-gray-900 text-sm sm:text-base">Transfers</p>
            </div>

            {/* Service 5 */}
            <div className="flex flex-col items-center text-center space-y-3">
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center">
                <Shield className="w-7 h-7 text-blue-600" />
              </div>
              <p className="font-semibold text-gray-900 text-sm sm:text-base">Visa & Insurance</p>
            </div>
          </div>

          {/* Decorative Wave at Bottom */}
          <div className="mt-16 relative h-32">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-blue-600 rounded-t-full opacity-90" />
            <div className="absolute inset-0 bg-gradient-to-r from-orange-400 to-orange-500 rounded-t-full opacity-30 translate-y-2" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white px-4 sm:px-6 lg:px-8 py-8">
        <div className="max-w-7xl mx-auto text-center text-gray-400 text-sm">
          <p>&copy; 2024 TBO Travel AI Copilot. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
