'use client'

import { SourceHealth } from '@/lib/api'
import { CheckCircle, XCircle, Clock, AlertTriangle } from 'lucide-react'

interface SourceHealthProps {
  sources: SourceHealth[]
}

export function SourceHealthList({ sources }: SourceHealthProps) {
  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'ok':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'skipped':
        return <Clock className="w-5 h-5 text-yellow-500" />
      default:
        return <AlertTriangle className="w-5 h-5 text-gray-500" />
    }
  }

  const getStatusBadgeColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'ok':
        return 'bg-green-100 text-green-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      case 'skipped':
        return 'bg-yellow-100 text-yellow-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getQuotaColor = (usagePercent?: number) => {
    if (!usagePercent) return 'bg-gray-200'
    if (usagePercent >= 90) return 'bg-red-500'
    if (usagePercent >= 75) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  return (
    <div className="space-y-3">
      {sources.map((source) => (
        <div key={source.name} className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center">
              {getStatusIcon(source.status)}
              <h3 className="ml-2 font-semibold text-gray-900 capitalize">{source.name}</h3>
            </div>
            <span
              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeColor(
                source.status
              )}`}
            >
              {source.status}
            </span>
          </div>

          {/* Quota Bar */}
          {source.quota.limit > 0 && (
            <div className="mb-3">
              <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                <span>Daily Quota</span>
                <span>
                  {source.quota.used} / {source.quota.limit}
                  {source.quota.usage_percent !== undefined && (
                    <span className="ml-1">({source.quota.usage_percent.toFixed(0)}%)</span>
                  )}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full transition-all ${getQuotaColor(source.quota.usage_percent)}`}
                  style={{
                    width: source.quota.usage_percent
                      ? `${Math.min(source.quota.usage_percent, 100)}%`
                      : '0%',
                  }}
                ></div>
              </div>
              {source.quota.usage_percent && source.quota.usage_percent > source.quota.stop_threshold * 100 && (
                <p className="text-xs text-orange-600 mt-1 flex items-center">
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  Approaching stop threshold ({(source.quota.stop_threshold * 100).toFixed(0)}%)
                </p>
              )}
            </div>
          )}

          {/* Message */}
          {source.message && (
            <p className="text-sm text-gray-600 mb-2">{source.message}</p>
          )}

          {/* Last Polled */}
          {source.last_polled_at && (
            <p className="text-xs text-gray-500">
              Last polled: {new Date(source.last_polled_at).toLocaleString()}
            </p>
          )}
        </div>
      ))}
    </div>
  )
}
