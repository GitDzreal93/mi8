'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

export function useSettings(category?: string) {
  return useQuery({
    queryKey: ['settings', category],
    queryFn: () => api.settings.getAll(category),
  })
}

export function useSettingsByCategory() {
  return useQuery({
    queryKey: ['settings-by-category'],
    queryFn: () => api.settings.getByCategory(),
  })
}

export function useInitSettings() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => api.settings.init(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] })
      queryClient.invalidateQueries({ queryKey: ['settings-by-category'] })
    },
  })
}

export function useUpdateSetting() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ key, value }: { key: string; value: any }) =>
      api.settings.update(key, value),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] })
      queryClient.invalidateQueries({ queryKey: ['settings-by-category'] })
    },
  })
}

export function useBulkUpdateSettings() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (configs: { key: string; value: any }[]) =>
      api.settings.bulkUpdate(configs),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['settings'] })
      queryClient.invalidateQueries({ queryKey: ['settings-by-category'] })
    },
  })
}

export function useRawItems(params?: {
  source?: string
  q?: string
  hours?: number
  limit?: number
  offset?: number
}) {
  return useQuery({
    queryKey: ['raw-items', params],
    queryFn: () => api.rawItems.list(params),
  })
}

export function useRawItemSources() {
  return useQuery({
    queryKey: ['raw-item-sources'],
    queryFn: () => api.rawItems.sources(),
  })
}

export function useRawItemsStats() {
  return useQuery({
    queryKey: ['raw-items-stats'],
    queryFn: () => api.rawItems.stats(),
  })
}
