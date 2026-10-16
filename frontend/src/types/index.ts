export interface Direction {title: string; slug: string; short_description: string; description: string; image?: string; order: number}
export interface ProjectImage {image: string; caption: string; order: number}
export interface Project {title: string; slug: string; short_description: string; description: string; completed_work: string; features: string; result: string; location: string; year?: number; cover_image?: string; featured: boolean; images: ProjectImage[]}
export interface Contact {company_name: string; phone: string; email: string; address: string; requisites: string}

