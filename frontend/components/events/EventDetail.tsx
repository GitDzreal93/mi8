'use client'

import { Event } from '@/lib/api'
import { X, Shield, MapPin, Clock, Building, Package, AlertCircle } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

interface EventDetailProps {
  event: Event | null
  onClose: () => void
}

export function EventDetail({ event, onClose }: EventDetailProps) {
  if (!event) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Event Details</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Title and Importance */}
          <div>
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-2xl font-bold text-gray-900 flex-1 pr-4">{event.title}</h3>
              {event.importance && (
                <div className="flex-shrink-0">
                  <span
                    className={`inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium ${
                      event.importance >= 5
                        ? 'bg-red-100 text-red-800'
                        : event.importance >= 4
                        ? 'bg-orange-100 text-orange-800'
                        : event.importance >= 3
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    <Shield className="w-4 h-4 mr-1.5" />
                    Importance: {event.importance}/5
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Summary */}
          {(event.summary_en || event.summary_zh) && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">Summary</h4>
              <p className="text-gray-600">{event.summary_en || event.summary_zh}</p>
            </div>
          )}

          {/* Event Type */}
          {event.event_type && (
            <div className="flex items-center">
              <span className="inline-flex items-center px-3 py-1.5 rounded-lg text-sm font-medium bg-blue-50 text-blue-700">
                {event.event_type}
              </span>
              {event.confidence && (
                <span className="ml-3 text-sm text-gray-500">
                  Confidence: {(event.confidence * 100).toFixed(0)}%
                </span>
              )}
            </div>
          )}

          {/* Location */}
          {event.location_lat && event.location_lng && (
            <div className="flex items-start">
              <MapPin className="w-5 h-5 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-semibold text-gray-700">Location</h4>
                <p className="text-gray-600">
                  {event.location_lat.toFixed(4)}, {event.location_lng.toFixed(4)}
                </p>
                {event.geo_precision && (
                  <p className="text-xs text-gray-500 mt-1">
                    Precision: {event.geo_precision}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Time */}
          {event.event_time && (
            <div className="flex items-start">
              <Clock className="w-5 h-5 text-gray-400 mr-2 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-semibold text-gray-700">Event Time</h4>
                <p className="text-gray-600">
                  {new Date(event.event_time).toLocaleString()}
                  <span className="text-gray-500 ml-2">
                    ({formatDistanceToNow(new Date(event.event_time), { addSuffix: true })})
                  </span>
                </p>
              </div>
            </div>
          )}

          {/* Actors */}
          {event.actors && event.actors.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                <Building className="w-4 h-4 mr-2" />
                Actors
              </h4>
              <div className="flex flex-wrap gap-2">
                {event.actors.map((actor) => (
                  <span
                    key={actor}
                    className="inline-flex items-center px-3 py-1 rounded-lg text-sm bg-gray-100 text-gray-700"
                  >
                    {actor}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Equipment */}
          {event.equipment && event.equipment.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                <Package className="w-4 h-4 mr-2" />
                Equipment
              </h4>
              <div className="flex flex-wrap gap-2">
                {event.equipment.map((equip) => (
                  <span
                    key={equip}
                    className="inline-flex items-center px-3 py-1 rounded-lg text-sm bg-gray-100 text-gray-700"
                  >
                    {equip}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Casualties */}
          {event.casualties && Object.keys(event.casualties).length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                <AlertCircle className="w-4 h-4 mr-2" />
                Casualties
              </h4>
              <div className="bg-red-50 border border-red-100 rounded-lg p-3">
                {Object.entries(event.casualties).map(([key, value]) => (
                  <div key={key} className="text-sm">
                    <span className="font-medium text-red-800">{key}:</span>{' '}
                    <span className="text-red-700">{String(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tags */}
          {event.tags && event.tags.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-700 mb-2">Tags</h4>
              <div className="flex flex-wrap gap-2">
                {event.tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center px-3 py-1 rounded-lg text-sm bg-blue-50 text-blue-700"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Source */}
          <div className="pt-4 border-t">
            <p className="text-xs text-gray-500">
              Source: <span className="font-medium">{event.source}</span>
              {event.created_at && (
                <span className="ml-3">
                  Added: {new Date(event.created_at).toLocaleString()}
                </span>
              )}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
