
export interface Venue {
  id: string;
  name: string;
  location: string;
  capacity: string;
  price: string;
  imageUrl: string;
  description: string;
  tags: string[];
  closestAirport: string; // e.g., "Marseille (45 mins)"
  ctaName?: string; // Shortened or personalized name for buttons
}

export interface NavLink {
  label: string;
  href: string;
}
