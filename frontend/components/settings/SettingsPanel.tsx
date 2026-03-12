'use client'

import { useState } from 'react'
import { useSettingsByCategory, useInitSettings, useUpdateSetting } from '@/hooks/use-settings'
import { ConfigCategory, ConfigItem } from '@/lib/api'
import {
  Settings,
  Key,
  Database,
  Brain,
  Globe,
  BarChart3,
  Timer,
  Shield,
  Bell,
  Monitor,
  Save,
  RefreshCw,
  Check,
  AlertTriangle,
  Eye,
  EyeOff,
  Loader2,
} from 'lucide-react'

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  app: <Monitor className="w-5 h-5" />,
  database: <Database className="w-5 h-5" />,
  llm: <Brain className="w-5 h-5" />,
  sources: <Globe className="w-5 h-5" />,
  quota: <BarChart3 className="w-5 h-5" />,
  polling: <Timer className="w-5 h-5" />,
  auth: <Shield className="w-5 h-5" />,
  alerts: <Bell className="w-5 h-5" />,
}

const CATEGORY_COLORS: Record<string, string> = {
  app: 'bg-gray-100 text-gray-700 border-gray-200',
  database: 'bg-blue-50 text-blue-700 border-blue-200',
  llm: 'bg-purple-50 text-purple-700 border-purple-200',
  sources: 'bg-green-50 text-green-700 border-green-200',
  quota: 'bg-orange-50 text-orange-700 border-orange-200',
  polling: 'bg-cyan-50 text-cyan-700 border-cyan-200',
  auth: 'bg-red-50 text-red-700 border-red-200',
  alerts: 'bg-yellow-50 text-yellow-700 border-yellow-200',
}

export function SettingsPanel() {
  const { data: categories, isLoading, error } = useSettingsByCategory()
  const initMutation = useInitSettings()
  const updateMutation = useUpdateSetting()

  const [editingValues, setEditingValues] = useState<Record<string, any>>({})
  const [revealedKeys, setRevealedKeys] = useState<Set<string>>(new Set())
  const [savedKeys, setSavedKeys] = useState<Set<string>>(new Set())
  const [activeCategory, setActiveCategory] = useState<string | null>(null)

  const handleInit = () => {
    initMutation.mutate()
  }

  const handleValueChange = (key: string, value: any) => {
    setEditingValues((prev) => ({ ...prev, [key]: value }))
    // Remove saved indicator when editing
    setSavedKeys((prev) => {
      const next = new Set(prev)
      next.delete(key)
      return next
    })
  }

  const handleSave = (key: string) => {
    const value = editingValues[key]
    if (value === undefined) return

    updateMutation.mutate(
      { key, value },
      {
        onSuccess: () => {
          setSavedKeys((prev) => new Set(prev).add(key))
          setEditingValues((prev) => {
            const next = { ...prev }
            delete next[key]
            return next
          })
          // Clear saved indicator after 2 seconds
          setTimeout(() => {
            setSavedKeys((prev) => {
              const next = new Set(prev)
              next.delete(key)
              return next
            })
          }, 2000)
        },
      }
    )
  }

  const toggleReveal = (key: string) => {
    setRevealedKeys((prev) => {
      const next = new Set(prev)
      if (next.has(key)) {
        next.delete(key)
      } else {
        next.add(key)
      }
      return next
    })
  }

  const getDisplayValue = (config: ConfigItem): string => {
    const editValue = editingValues[config.key]
    const currentValue = editValue !== undefined ? editValue : config.value

    if (currentValue === null || currentValue === undefined) return ''
    if (typeof currentValue === 'boolean') return currentValue ? 'true' : 'false'
    return String(currentValue)
  }

  const parseInputValue = (config: ConfigItem, inputValue: string): any => {
    const originalValue = config.value
    if (typeof originalValue === 'number') {
      const num = Number(inputValue)
      return isNaN(num) ? inputValue : num
    }
    if (typeof originalValue === 'boolean') {
      return inputValue === 'true'
    }
    return inputValue
  }

  const hasUnsavedChanges = (key: string) => {
    return editingValues[key] !== undefined
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-gray-400 animate-spin" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Settings Not Initialized</h3>
          <p className="text-gray-600 mb-6">
            Click the button below to initialize default configurations from environment variables.
          </p>
          <button
            onClick={handleInit}
            disabled={initMutation.isPending}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors inline-flex items-center"
          >
            {initMutation.isPending ? (
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            ) : (
              <Settings className="w-5 h-5 mr-2" />
            )}
            Initialize Settings
          </button>
          {initMutation.isSuccess && (
            <p className="mt-4 text-green-600">✅ Settings initialized successfully!</p>
          )}
        </div>
      </div>
    )
  }

  if (!categories || categories.length === 0) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-sm p-8 text-center">
          <Settings className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Settings Found</h3>
          <p className="text-gray-600 mb-6">Initialize default settings to get started.</p>
          <button
            onClick={handleInit}
            disabled={initMutation.isPending}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 transition-colors inline-flex items-center"
          >
            {initMutation.isPending ? (
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            ) : (
              <RefreshCw className="w-5 h-5 mr-2" />
            )}
            Initialize Defaults
          </button>
        </div>
      </div>
    )
  }

  const displayCategories = activeCategory
    ? categories.filter((c) => c.category === activeCategory)
    : categories

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-900 flex items-center">
              <Settings className="w-6 h-6 mr-2 text-blue-600" />
              System Settings
            </h2>
            <p className="text-gray-600 mt-1">Configure API keys, quotas, and system parameters</p>
          </div>
          <button
            onClick={handleInit}
            disabled={initMutation.isPending}
            className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors inline-flex items-center"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${initMutation.isPending ? 'animate-spin' : ''}`} />
            Re-initialize
          </button>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setActiveCategory(null)}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              activeCategory === null
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            All
          </button>
          {categories.map((cat) => (
            <button
              key={cat.category}
              onClick={() => setActiveCategory(cat.category)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors inline-flex items-center ${
                activeCategory === cat.category
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <span className="mr-1.5">{CATEGORY_ICONS[cat.category] || <Key className="w-4 h-4" />}</span>
              {cat.description}
            </button>
          ))}
        </div>
      </div>

      {/* Settings Groups */}
      <div className="space-y-6">
        {displayCategories.map((cat) => (
          <div key={cat.category} className="bg-white rounded-lg shadow-sm overflow-hidden">
            {/* Category Header */}
            <div className={`px-6 py-4 border-b ${CATEGORY_COLORS[cat.category] || 'bg-gray-50 text-gray-700 border-gray-200'}`}>
              <div className="flex items-center">
                {CATEGORY_ICONS[cat.category] || <Key className="w-5 h-5" />}
                <h3 className="ml-2 font-semibold">{cat.description}</h3>
                <span className="ml-2 text-xs opacity-70">({cat.configs.length} items)</span>
              </div>
            </div>

            {/* Config Items */}
            <div className="divide-y divide-gray-100">
              {cat.configs.map((config) => (
                <div key={config.key} className="px-6 py-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <code className="text-sm font-mono text-gray-800 bg-gray-100 px-2 py-0.5 rounded">
                          {config.key}
                        </code>
                        {config.is_sensitive && (
                          <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-red-50 text-red-600">
                            <Key className="w-3 h-3 mr-0.5" />
                            sensitive
                          </span>
                        )}
                        {savedKeys.has(config.key) && (
                          <span className="inline-flex items-center text-xs text-green-600">
                            <Check className="w-3 h-3 mr-0.5" />
                            saved
                          </span>
                        )}
                      </div>
                      {config.description && (
                        <p className="text-sm text-gray-500">{config.description}</p>
                      )}
                    </div>

                    <div className="flex items-center gap-2 flex-shrink-0">
                      {/* Value Input */}
                      {typeof config.value === 'boolean' ? (
                        <select
                          value={getDisplayValue(config)}
                          onChange={(e) =>
                            handleValueChange(config.key, e.target.value === 'true')
                          }
                          className="w-24 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                          <option value="true">true</option>
                          <option value="false">false</option>
                        </select>
                      ) : (
                        <div className="relative">
                          <input
                            type={config.is_sensitive && !revealedKeys.has(config.key) ? 'password' : 'text'}
                            value={getDisplayValue(config)}
                            onChange={(e) =>
                              handleValueChange(config.key, parseInputValue(config, e.target.value))
                            }
                            className={`w-64 px-3 py-2 border rounded-lg text-sm font-mono focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                              hasUnsavedChanges(config.key)
                                ? 'border-yellow-400 bg-yellow-50'
                                : 'border-gray-300'
                            }`}
                            placeholder="(empty)"
                          />
                          {config.is_sensitive && (
                            <button
                              onClick={() => toggleReveal(config.key)}
                              className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                            >
                              {revealedKeys.has(config.key) ? (
                                <EyeOff className="w-4 h-4" />
                              ) : (
                                <Eye className="w-4 h-4" />
                              )}
                            </button>
                          )}
                        </div>
                      )}

                      {/* Save Button */}
                      <button
                        onClick={() => handleSave(config.key)}
                        disabled={!hasUnsavedChanges(config.key) || updateMutation.isPending}
                        className={`p-2 rounded-lg transition-colors ${
                          hasUnsavedChanges(config.key)
                            ? 'bg-blue-600 text-white hover:bg-blue-700'
                            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        }`}
                        title="Save"
                      >
                        <Save className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
