'use client'

import { useState } from 'react'
import { useEvents, useHeatmap, useSourceHealth, useEventTypes, useEventSources, useSystemStats, useRefreshData } from '@/hooks/use-events'
import { EventMap } from '@/components/map/EventMap'
import { EventList } from '@/components/events/EventList'
import { EventDetail } from '@/components/events/EventDetail'
import { EventFilters, FilterState } from '@/components/events/EventFilters'
import { SourceHealthList } from '@/components/sources/SourceHealth'
import { SettingsPanel } from '@/components/settings/SettingsPanel'
import { DataExplorer } from '@/components/data/DataExplorer'
import { Event } from '@/lib/api'
import { Activity, TrendingUp, AlertTriangle, Database, RefreshCw, Shield, Settings, FileSearch } from 'lucide-react'

type TabType = 'dashboard' | 'sources' | 'data' | 'settings'

export default function Home() {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('dashboard')
  const [filters, setFilters] = useState<FilterState>({
    hours: 24,
    importance: undefined,
    event_type: undefined,
    source: undefined,
    q: '',
  })

  const { data: events, isLoading: eventsLoading } = useEvents({
    hours: filters.hours,
    importance: filters.importance,
    event_type: filters.event_type,
    source: filters.source,
    q: filters.q || undefined,
    limit: 100,
  })

  const { data: heatmapData } = useHeatmap({
    hours: filters.hours,
    importance: filters.importance,
  })

  const { data: sourceHealth } = useSourceHealth()
  const { data: eventTypes } = useEventTypes()
  const { data: eventSources } = useEventSources()
  const { data: stats } = useSystemStats()
  const refreshMutation = useRefreshData()

  const eventsList = events || []

  const tabs: { key: TabType; label: string; icon: React.ReactNode }[] = [
    { key: 'dashboard', label: 'Dashboard', icon: <Activity className="w-4 h-4 mr-1.5" /> },
    { key: 'sources', label: 'Data Sources', icon: <Database className="w-4 h-4 mr-1.5" /> },
    { key: 'data', label: 'Data Explorer', icon: <FileSearch className="w-4 h-4 mr-1.5" /> },
    { key: 'settings', label: 'Settings', icon: <Settings className="w-4 h-4 mr-1.5" /> },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-40">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Military Intelligence Dashboard</h1>
            </div>
            <div className="flex items-center space-x-2">
              {tabs.map((tab) => (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm inline-flex items-center ${
                    activeTab === tab.key
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
              <div className="w-px h-8 bg-gray-200 mx-2" />
              <button
                onClick={() => refreshMutation.mutate()}
                disabled={refreshMutation.isPending}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors flex items-center text-sm"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${refreshMutation.isPending ? 'animate-spin' : ''}`} />
                Refresh
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Stats Cards */}
        {activeTab === 'dashboard' && stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Events</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_events}</p>
                </div>
                <Database className="w-8 h-8 text-blue-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Last 24h</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.recent_events_24h}</p>
                </div>
                <Activity className="w-8 h-8 text-green-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">High Importance</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.high_importance_events}</p>
                </div>
                <AlertTriangle className="w-8 h-8 text-orange-500" />
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Raw Items</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_raw_items}</p>
                </div>
                <TrendingUp className="w-8 h-8 text-purple-500" />
              </div>
            </div>
          </div>
        )}

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column: Map and Filters */}
            <div className="lg:col-span-2 space-y-6">
              {/* Map */}
              <div className="bg-white rounded-lg shadow-sm p-4">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Event Map</h2>
                <EventMap events={eventsList} onEventClick={setSelectedEvent} />
              </div>

              {/* Filters */}
              <EventFilters
                filters={filters}
                onFiltersChange={setFilters}
                eventTypes={eventTypes?.types}
                sources={eventSources?.sources}
              />
            </div>

            {/* Right Column: Event List */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm p-4 sticky top-24">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Events ({eventsList.length})
                </h2>
                {eventsLoading ? (
                  <div className="flex items-center justify-center h-64">
                    <RefreshCw className="w-8 h-8 text-gray-400 animate-spin" />
                  </div>
                ) : (
                  <EventList events={eventsList} onEventClick={setSelectedEvent} />
                )}
              </div>
            </div>
          </div>
        )}

        {/* Sources Tab */}
        {activeTab === 'sources' && sourceHealth && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <h2 className="text-xl font-bold text-gray-900 mb-2">Data Source Health</h2>
              <p className="text-gray-600">
                Monitor the status and quota usage of all data sources
              </p>
            </div>
            <SourceHealthList sources={sourceHealth.sources} />
          </div>
        )}

        {/* Data Explorer Tab */}
        {activeTab === 'data' && <DataExplorer />}

        {/* Settings Tab */}
        {activeTab === 'settings' && <SettingsPanel />}
      </main>

      {/* Event Detail Modal */}
      <EventDetail event={selectedEvent} onClose={() => setSelectedEvent(null)} />
    </div>
  )
}
