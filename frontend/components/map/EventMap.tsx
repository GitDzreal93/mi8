'use client'

import dynamic from 'next/dynamic'
import { Event } from '@/lib/api'
import { RefreshCw } from 'lucide-react'

const EventMapInner = dynamic(() => import('./EventMapInner'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center bg-gray-100 rounded-lg" style={{ height: '600px' }}>
      <RefreshCw className="w-8 h-8 text-gray-400 animate-spin" />
    </div>
  ),
})

interface EventMapProps {
  events: Event[]
  onEventClick?: (event: Event) => void
  height?: string
}

export function EventMap({ events, onEventClick, height = '600px' }: EventMapProps) {
  return <EventMapInner events={events} onEventClick={onEventClick} height={height} />
}
