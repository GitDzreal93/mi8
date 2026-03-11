'use client'

import { Event } from '@/lib/api'
import { formatDistanceToNow } from 'date-fns'
import { Shield, Clock, MapPin } from 'lucide-react'

interface EventListProps {
  events: Event[]
  onEventClick?: (event: Event) => void
}

export function EventList({ events, onEventClick }: EventListProps) {
  if (events.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500">
        <p>No events found</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {events.map((event) => (
        <div
          key={event.id}
          onClick={() => onEventClick?.(event)}
          className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer p-4"
        >
          <div className="flex items-start justify-between mb-2">
            <h3 className="font-semibold text-gray-900 flex-1 pr-2 line-clamp-2">
              {event.title}
            </h3>
            {event.importance && (
              <div className="flex-shrink-0">
                <span
                  className={`inline-flex items-center px-2 py-1 rounded text-xs font-medium ${
                    event.importance >= 5
                      ? 'bg-red-100 text-red-800'
                      : event.importance >= 4
                      ? 'bg-orange-100 text-orange-800'
                      : event.importance >= 3
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-blue-100 text-blue-800'
                  }`}
                >
                  <Shield className="w-3 h-3 mr-1" />
                  {event.importance}
                </span>
              </div>
            )}
          </div>

          {event.summary_en && (
            <p className="text-sm text-gray-600 mb-3 line-clamp-2">
              {event.summary_en}
            </p>
          )}

          <div className="flex items-center justify-between text-xs text-gray-500">
            <div className="flex items-center space-x-3">
              {event.event_type && (
                <span className="inline-block bg-gray-100 px-2 py-1 rounded">
                  {event.event_type}
                </span>
              )}
              {event.source && (
                <span className="inline-block bg-gray-100 px-2 py-1 rounded">
                  {event.source}
                </span>
              )}
              {event.location_lat && event.location_lng && (
                <span className="flex items-center">
                  <MapPin className="w-3 h-3 mr-1" />
                  {event.location_lat.toFixed(2)}, {event.location_lng.toFixed(2)}
                </span>
              )}
            </div>
            {event.event_time && (
              <span className="flex items-center">
                <Clock className="w-3 h-3 mr-1" />
                {formatDistanceToNow(new Date(event.event_time), { addSuffix: true })}
              </span>
            )}
          </div>

          {event.confidence && (
            <div className="mt-2">
              <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                <span>Confidence</span>
                <span>{(event.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-blue-500 h-1.5 rounded-full"
                  style={{ width: `${event.confidence * 100}%` }}
                ></div>
              </div>
            </div>
          )}

          {event.tags && event.tags.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {event.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center px-2 py-0.5 rounded text-xs bg-blue-50 text-blue-700"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
