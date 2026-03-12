'use client'

import { useState } from 'react'
import { useRawItems, useRawItemSources, useRawItemsStats } from '@/hooks/use-settings'
import { RawItem } from '@/lib/api'
import { formatDistanceToNow } from 'date-fns'
import {
  Search,
  ExternalLink,
  Clock,
  Database,
  ChevronLeft,
  ChevronRight,
  TrendingUp,
  FileText,
  Loader2,
  X,
  Filter,
} from 'lucide-react'

export function DataExplorer() {
  const [selectedSource, setSelectedSource] = useState<string | undefined>(undefined)
  const [searchQuery, setSearchQuery] = useState('')
  const [currentPage, setCurrentPage] = useState(0)
  const [expandedItem, setExpandedItem] = useState<string | null>(null)
  const pageSize = 20

  const { data: rawItemsData, isLoading } = useRawItems({
    source: selectedSource,
    q: searchQuery || undefined,
    limit: pageSize,
    offset: currentPage * pageSize,
  })

  const { data: sourcesData } = useRawItemSources()
  const { data: statsData } = useRawItemsStats()

  const items = rawItemsData?.items || []
  const totalItems = rawItemsData?.total || 0
  const totalPages = Math.ceil(totalItems / pageSize)

  const sources = sourcesData?.sources || []

  const handleSourceFilter = (source: string | undefined) => {
    setSelectedSource(source)
    setCurrentPage(0)
  }

  const handleSearch = (q: string) => {
    setSearchQuery(q)
    setCurrentPage(0)
  }

  const getSourceColor = (source: string) => {
    const colors: Record<string, string> = {
      gnews: 'bg-blue-100 text-blue-800',
      newsapi: 'bg-green-100 text-green-800',
      acled: 'bg-red-100 text-red-800',
      rsshub: 'bg-orange-100 text-orange-800',
      firms: 'bg-purple-100 text-purple-800',
    }
    return colors[source] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header & Stats */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 flex items-center">
              <Database className="w-6 h-6 mr-2 text-blue-600" />
              Data Explorer
            </h2>
            <p className="text-gray-600 mt-1">Browse and search raw data items from all sources</p>
          </div>
        </div>

        {/* Summary Stats */}
        {statsData && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-xs text-blue-600 font-medium">Total Items</p>
              <p className="text-2xl font-bold text-blue-900">{statsData.total.toLocaleString()}</p>
            </div>
            <div className="bg-green-50 rounded-lg p-3">
              <p className="text-xs text-green-600 font-medium">Last 24h</p>
              <p className="text-2xl font-bold text-green-900">{statsData.recent_24h.toLocaleString()}</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-3">
              <p className="text-xs text-purple-600 font-medium">Sources</p>
              <p className="text-2xl font-bold text-purple-900">{statsData.by_source.length}</p>
            </div>
            <div className="bg-orange-50 rounded-lg p-3">
              <p className="text-xs text-orange-600 font-medium">
                Latest
              </p>
              <p className="text-sm font-bold text-orange-900 mt-1">
                {statsData.by_source.length > 0 && statsData.by_source[0].latest
                  ? formatDistanceToNow(new Date(statsData.by_source[0].latest), { addSuffix: true })
                  : 'N/A'}
              </p>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Sidebar: Sources */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm p-4 sticky top-24">
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
              <Filter className="w-4 h-4 mr-2" />
              Sources
            </h3>

            <div className="space-y-1">
              <button
                onClick={() => handleSourceFilter(undefined)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-between ${
                  !selectedSource
                    ? 'bg-blue-100 text-blue-700 font-medium'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <span>All Sources</span>
                <span className="text-xs">{totalItems.toLocaleString()}</span>
              </button>

              {sources.map((src) => (
                <button
                  key={src.name}
                  onClick={() => handleSourceFilter(src.name)}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors flex items-center justify-between ${
                    selectedSource === src.name
                      ? 'bg-blue-100 text-blue-700 font-medium'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <span className="capitalize">{src.name}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${getSourceColor(src.name)}`}>
                    {src.count.toLocaleString()}
                  </span>
                </button>
              ))}
            </div>

            {/* Source Stats */}
            {statsData && statsData.by_source.length > 0 && (
              <div className="mt-6 pt-4 border-t">
                <h4 className="text-xs font-semibold text-gray-500 uppercase mb-3 flex items-center">
                  <TrendingUp className="w-3 h-3 mr-1" />
                  By Volume
                </h4>
                <div className="space-y-2">
                  {statsData.by_source.map((s) => {
                    const maxCount = statsData.by_source[0]?.count || 1
                    const widthPercent = (s.count / maxCount) * 100
                    return (
                      <div key={s.source}>
                        <div className="flex justify-between text-xs text-gray-600 mb-1">
                          <span className="capitalize">{s.source}</span>
                          <span>{s.count.toLocaleString()}</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-1.5">
                          <div
                            className="bg-blue-500 h-1.5 rounded-full transition-all"
                            style={{ width: `${widthPercent}%` }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3 space-y-4">
          {/* Search Bar */}
          <div className="bg-white rounded-lg shadow-sm p-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Search raw items by title or content..."
                className="w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              {searchQuery && (
                <button
                  onClick={() => handleSearch('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>
            <div className="flex items-center justify-between mt-3 text-sm text-gray-500">
              <span>
                Showing {items.length} of {totalItems.toLocaleString()} items
                {selectedSource && (
                  <span className="ml-1">
                    from <span className="font-medium capitalize">{selectedSource}</span>
                  </span>
                )}
              </span>
              {selectedSource && (
                <button
                  onClick={() => handleSourceFilter(undefined)}
                  className="text-blue-600 hover:text-blue-800 text-xs"
                >
                  Clear filter
                </button>
              )}
            </div>
          </div>

          {/* Items List */}
          {isLoading ? (
            <div className="bg-white rounded-lg shadow-sm p-12 flex items-center justify-center">
              <Loader2 className="w-8 h-8 text-gray-400 animate-spin" />
            </div>
          ) : items.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No raw items found</p>
            </div>
          ) : (
            <div className="space-y-3">
              {items.map((item) => (
                <RawItemCard
                  key={item.id}
                  item={item}
                  expanded={expandedItem === item.id}
                  onToggle={() => setExpandedItem(expandedItem === item.id ? null : item.id)}
                  getSourceColor={getSourceColor}
                />
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="bg-white rounded-lg shadow-sm p-4 flex items-center justify-between">
              <button
                onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                disabled={currentPage === 0}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                <ChevronLeft className="w-4 h-4 mr-1" />
                Previous
              </button>

              <div className="flex items-center gap-1">
                {Array.from({ length: Math.min(totalPages, 7) }, (_, i) => {
                  let pageNum: number
                  if (totalPages <= 7) {
                    pageNum = i
                  } else if (currentPage < 3) {
                    pageNum = i
                  } else if (currentPage > totalPages - 4) {
                    pageNum = totalPages - 7 + i
                  } else {
                    pageNum = currentPage - 3 + i
                  }
                  return (
                    <button
                      key={pageNum}
                      onClick={() => setCurrentPage(pageNum)}
                      className={`w-8 h-8 text-sm rounded-lg ${
                        currentPage === pageNum
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {pageNum + 1}
                    </button>
                  )
                })}
              </div>

              <button
                onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
                disabled={currentPage >= totalPages - 1}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                Next
                <ChevronRight className="w-4 h-4 ml-1" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function RawItemCard({
  item,
  expanded,
  onToggle,
  getSourceColor,
}: {
  item: RawItem
  expanded: boolean
  onToggle: () => void
  getSourceColor: (source: string) => string
}) {
  return (
    <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden">
      <div className="p-4 cursor-pointer" onClick={onToggle}>
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 line-clamp-2 text-sm">{item.title}</h3>
            {!expanded && item.content && (
              <p className="text-sm text-gray-500 mt-1 line-clamp-1">{item.content}</p>
            )}
          </div>
          <span
            className={`flex-shrink-0 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium capitalize ${getSourceColor(
              item.source
            )}`}
          >
            {item.source}
          </span>
        </div>

        <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
          {item.published_at && (
            <span className="flex items-center">
              <Clock className="w-3 h-3 mr-1" />
              {formatDistanceToNow(new Date(item.published_at), { addSuffix: true })}
            </span>
          )}
          {item.url && (
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="flex items-center text-blue-600 hover:text-blue-800"
            >
              <ExternalLink className="w-3 h-3 mr-1" />
              Source
            </a>
          )}
          {item.source_id && (
            <span className="text-gray-400 font-mono truncate max-w-[200px]">
              ID: {item.source_id}
            </span>
          )}
        </div>
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div className="border-t bg-gray-50 px-4 py-3">
          {item.content && (
            <div className="mb-3">
              <h4 className="text-xs font-semibold text-gray-500 uppercase mb-1">Content</h4>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{item.content}</p>
            </div>
          )}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="font-semibold text-gray-500">Created:</span>{' '}
              <span className="text-gray-700">
                {item.created_at ? new Date(item.created_at).toLocaleString() : 'N/A'}
              </span>
            </div>
            <div>
              <span className="font-semibold text-gray-500">Published:</span>{' '}
              <span className="text-gray-700">
                {item.published_at ? new Date(item.published_at).toLocaleString() : 'N/A'}
              </span>
            </div>
            {item.hash_key && (
              <div className="col-span-2">
                <span className="font-semibold text-gray-500">Hash:</span>{' '}
                <code className="text-gray-600 font-mono text-xs">{item.hash_key}</code>
              </div>
            )}
          </div>
          {item.url && (
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-xs rounded-lg hover:bg-blue-700 transition-colors"
            >
              <ExternalLink className="w-3 h-3 mr-1.5" />
              Open Original
            </a>
          )}
        </div>
      )}
    </div>
  )
}
