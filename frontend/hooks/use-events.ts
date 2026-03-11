'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api, Event } from '@/lib/api'

export function useEvents(params?: {
  importance?: number
  event_type?: string
  source?: string
  tags?: string
  q?: string
  hours?: number
  limit?: number
}) {
  return useQuery({
    queryKey: ['events', params],
    queryFn: () => api.events.list(params),
  })
}

export function useEvent(id: string) {
  return useQuery({
    queryKey: ['event', id],
    queryFn: () => api.events.get(id),
    enabled: !!id,
  })
}

export function useEventTypes() {
  return useQuery({
    queryKey: ['event-types'],
    queryFn: () => api.events.getTypes(),
  })
}

export function useEventSources() {
  return useQuery({
    queryKey: ['event-sources'],
    queryFn: () => api.events.getSources(),
  })
}

export function useHeatmap(params?: {
  hours?: number
  importance?: number
  limit?: number
}) {
  return useQuery({
    queryKey: ['heatmap', params],
    queryFn: () => api.heatmap.geojson(params),
    refetchInterval: 60000, // Refetch every minute
  })
}

export function useSourceHealth() {
  return useQuery({
    queryKey: ['source-health'],
    queryFn: () => api.sources.health(),
    refetchInterval: 60000, // Refetch every minute
  })
}

export function useSystemStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: () => api.admin.stats(),
    refetchInterval: 60000, // Refetch every minute
  })
}

export function useRefreshData() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (token?: string) => api.admin.refresh(token),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['events'] })
      queryClient.invalidateQueries({ queryKey: ['heatmap'] })
      queryClient.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}
