'use client'

import { useState } from 'react'
import { Filter, X } from 'lucide-react'

export interface FilterState {
  hours: number | undefined
  importance: number | undefined
  event_type: string | undefined
  source: string | undefined
  q: string
}

interface EventFiltersProps {
  filters: FilterState
  onFiltersChange: (filters: FilterState) => void
  eventTypes?: string[]
  sources?: string[]
}

export function EventFilters({
  filters,
  onFiltersChange,
  eventTypes = [],
  sources = [],
}: EventFiltersProps) {
  const [isOpen, setIsOpen] = useState(false)

  const timeRanges = [
    { label: 'All Time', value: undefined },
    { label: 'Last Hour', value: 1 },
    { label: 'Last 6 Hours', value: 6 },
    { label: 'Last 24 Hours', value: 24 },
    { label: 'Last 7 Days', value: 168 },
  ]

  const importanceLevels = [
    { label: 'All', value: undefined },
    { label: 'High (4-5)', value: 4 },
    { label: 'Medium (3-4)', value: 3 },
    { label: 'Low (1-2)', value: 1 },
  ]

  const hasActiveFilters =
    filters.hours !== undefined ||
    filters.importance !== undefined ||
    filters.event_type !== undefined ||
    filters.source !== undefined ||
    filters.q !== ''

  const clearFilters = () => {
    onFiltersChange({
      hours: undefined,
      importance: undefined,
      event_type: undefined,
      source: undefined,
      q: '',
    })
  }

  return (
    <div className="bg-white rounded-lg shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors rounded-lg"
      >
        <div className="flex items-center">
          <Filter className="w-5 h-5 mr-2 text-gray-500" />
          <span className="font-medium text-gray-700">Filters</span>
          {hasActiveFilters && (
            <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full">
              Active
            </span>
          )}
        </div>
        <span className="text-gray-400">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="px-4 pb-4 space-y-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              value={filters.q}
              onChange={(e) => onFiltersChange({ ...filters, q: e.target.value })}
              placeholder="Search events..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {/* Time Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Time Range
            </label>
            <select
              value={filters.hours ?? 'all'}
              onChange={(e) =>
                onFiltersChange({
                  ...filters,
                  hours: e.target.value === 'all' ? undefined : Number(e.target.value),
                })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {timeRanges.map((range) => (
                <option key={range.label} value={range.value ?? 'all'}>
                  {range.label}
                </option>
              ))}
            </select>
          </div>

          {/* Importance */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Importance
            </label>
            <select
              value={filters.importance ?? 'all'}
              onChange={(e) =>
                onFiltersChange({
                  ...filters,
                  importance: e.target.value === 'all' ? undefined : Number(e.target.value),
                })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {importanceLevels.map((level) => (
                <option key={level.label} value={level.value ?? 'all'}>
                  {level.label}
                </option>
              ))}
            </select>
          </div>

          {/* Event Type */}
          {eventTypes.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Event Type
              </label>
              <select
                value={filters.event_type ?? 'all'}
                onChange={(e) =>
                  onFiltersChange({
                    ...filters,
                    event_type: e.target.value === 'all' ? undefined : e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Types</option>
                {eventTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Source */}
          {sources.length > 0 && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Source
              </label>
              <select
                value={filters.source ?? 'all'}
                onChange={(e) =>
                  onFiltersChange({
                    ...filters,
                    source: e.target.value === 'all' ? undefined : e.target.value,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All Sources</option>
                {sources.map((source) => (
                  <option key={source} value={source}>
                    {source}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Clear Button */}
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center"
            >
              <X className="w-4 h-4 mr-2" />
              Clear Filters
            </button>
          )}
        </div>
      )}
    </div>
  )
}
