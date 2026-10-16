import type {Contact, Direction, Project} from '../types'
const API_URL = import.meta.env.VITE_API_URL || '/api'

async function getJson<T>(path: string, fallback: T): Promise<T> {
  try { const response = await fetch(`${API_URL}${path}`); if (!response.ok) throw new Error(); return await response.json() }
  catch { return fallback }
}

export const fallbackDirection: Direction = {title: 'Архитектурные металлоконструкции и благоустройство', slug: 'architectural-metalworks', short_description: 'Конструкции для общественных пространств: от инженерной проработки до изготовления и монтажа.', description: '', order: 0}
export const fallbackContact: Contact = {company_name: 'ООО «КУДЛАЙН»', phone: '+7 911 134-26-37', email: 'kudline@inbox.ru', address: 'г. Выборг, ул. Промышленная, д. 19', requisites: ''}

export const api = {
  directions: () => getJson<Direction[]>('/services/', [fallbackDirection]),
  service: (slug: string) => getJson<Direction | null>(`/services/${slug}/`, null),
  projects: (featured = false) => getJson<Project[]>(`/projects/${featured ? '?featured=true' : ''}`, []),
  project: (slug: string) => getJson<Project | null>(`/projects/${slug}/`, null),
  contacts: async () => (await getJson<Contact[]>('/contacts/', [fallbackContact]))[0] || fallbackContact,
  sendInquiry: async (data: FormData) => {
    const response = await fetch(`${API_URL}/inquiries/`, {method: 'POST', body: data})
    if (!response.ok) { const errors = await response.json().catch(() => ({})); throw new Error(Object.values(errors).flat().join(' ') || 'Не удалось отправить заявку') }
    return response.json()
  }
}

