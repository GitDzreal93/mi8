'use client'

import { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Event } from '@/lib/api'

// Fix for default marker icons in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

function MapUpdater({ events }: { events: Event[] }) {
  const map = useMap()

  useEffect(() => {
    if (events.length > 0) {
      const validEvents = events.filter((e) => e.location_lat && e.location_lng)
      if (validEvents.length > 0) {
        const bounds = L.latLngBounds(
          validEvents.map((e) => [e.location_lat!, e.location_lng!] as [number, number])
        )
        map.fitBounds(bounds, { padding: [50, 50] })
      }
    }
  }, [events, map])

  return null
}

interface EventMapInnerProps {
  events: Event[]
  onEventClick?: (event: Event) => void
  height?: string
}

export default function EventMapInner({ events, onEventClick, height = '600px' }: EventMapInnerProps) {
  const validEvents = events.filter((e) => e.location_lat && e.location_lng)

  const getMarkerColor = (importance?: number) => {
    if (!importance) return '#3b82f6'
    if (importance >= 5) return '#dc2626'
    if (importance >= 4) return '#f97316'
    if (importance >= 3) return '#eab308'
    return '#3b82f6'
  }

  const createCustomIcon = (importance?: number) => {
    const color = getMarkerColor(importance)
    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      "></div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    })
  }

  return (
    <MapContainer
      center={[20, 0]}
      zoom={2}
      style={{ height, width: '100%' }}
      className="rounded-lg shadow-md"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapUpdater events={validEvents} />
      {validEvents.map((event) => (
        <Marker
          key={event.id}
          position={[event.location_lat!, event.location_lng!]}
          icon={createCustomIcon(event.importance)}
          eventHandlers={{
            click: () => onEventClick?.(event),
          }}
        >
          <Popup>
            <div className="p-2 min-w-[200px]">
              <h3 className="font-semibold text-sm mb-1">{event.title}</h3>
              <p className="text-xs text-gray-600 mb-2">
                {event.event_type && (
                  <span className="inline-block bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-xs mr-1">
                    {event.event_type}
                  </span>
                )}
                {event.importance && (
                  <span className="inline-block bg-orange-100 text-orange-800 px-2 py-0.5 rounded text-xs">
                    Imp: {event.importance}
                  </span>
                )}
              </p>
              {event.event_time && (
                <p className="text-xs text-gray-500">
                  {new Date(event.event_time).toLocaleString()}
                </p>
              )}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
