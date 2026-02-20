
import { Venue, NavLink } from './types';

// Exporting the list of venues for display in the app
export const VENUES: Venue[] = [
  {
    id: '1',
    name: 'Château de la Croix',
    ctaName: 'Château de la Croix',
    location: 'Provence',
    capacity: '150',
    price: '€12,000 / 2 nights',
    imageUrl: 'https://images.unsplash.com/photo-1542662565-7e4b66bae529?q=80&w=2000&auto=format&fit=crop',
    description: 'A magnificent 18th-century château nestled in the heart of Provence, surrounded by lavender fields and ancient olive groves. It offers a unique blend of historical grandeur and intimate rustic charm, perfect for couples seeking an authentic French experience. The estate features a grand reception hall with original stonework and multiple outdoor terraces for a sunset Vin d\'Honneur.',
    tags: ['Romantic', 'Historic'],
    closestAirport: 'Marseille (55 mins)'
  },
  {
    id: '2',
    name: 'Villa Ephrussi de Rothschild',
    ctaName: 'Villa Ephrussi',
    location: 'French Riviera',
    capacity: '300',
    price: 'On Request',
    imageUrl: 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?q=80&w=2000&auto=format&fit=crop',
    description: 'One of the most prestigious venues on the Côte d\'Azur, offering breathtaking sea views and nine themed gardens. This pink palace is the epitome of Riviera glamour and Belle Époque elegance. Guests can dine amidst musical fountains and rare botanical species, creating a truly sensory experience that is unmatched in European destination weddings.',
    tags: ['Coastal Elegance', 'Gardens'],
    closestAirport: 'Nice (25 mins)'
  },
  {
    id: '3',
    name: 'Domaine de Canaille',
    ctaName: 'Domaine de Canaille',
    location: 'Cassis',
    capacity: '80',
    price: '€15,000 / 3 nights',
    imageUrl: 'https://images.unsplash.com/photo-1544971582-674ca6b7b743?q=80&w=2000&auto=format&fit=crop',
    description: 'A cliffside gem overlooking the Mediterranean, perfect for intimate weddings with a modern, chic aesthetic. The infinity pool and dramatic limestone backdrop provide unparalleled photo opportunities. This private estate offers total seclusion and a minimalist architectural style that allows the natural beauty of the Calanques to take center stage.',
    tags: ['Cliffside', 'Modernity'],
    closestAirport: 'Marseille (40 mins)'
  },
  {
    id: '4',
    name: 'Château de Robernier',
    ctaName: 'Château de Robernier',
    location: 'Cotignac',
    capacity: '200',
    price: '€18,000 / 3 nights',
    imageUrl: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2000&auto=format&fit=crop',
    description: 'A fairytale castle hidden in the Provençal countryside, offering multiple spaces for ceremony and reception. Its distinctive turrets and private consecrated chapel make it a truly magical setting. The château has been lovingly restored to include high-end guest accommodations, allowing the bridal party to reside within the castle walls for the duration of the celebrations.',
    tags: ['Fairytale', 'Privacy'],
    closestAirport: 'Toulon-Hyères (50 mins)'
  },
  {
    id: '5',
    name: 'Bastide Saint-Mathieu',
    ctaName: 'Bastide Saint-Mathieu',
    location: 'Grasse',
    capacity: '120',
    price: '€9,000 / 2 nights',
    imageUrl: 'https://images.unsplash.com/photo-1505944270255-bd2b68af642d?q=80&w=2000&auto=format&fit=crop',
    description: 'A charming 18th-century manor house located near the perfume capital of Grasse, known for its warm atmosphere and exquisite cuisine prepared with local seasonal ingredients. The venue features a classic courtyard shaded by century-old plane trees, ideal for a traditional long-table Provencal wedding breakfast under fairy lights.',
    tags: ['Authentic', 'Provençal'],
    closestAirport: 'Nice (35 mins)'
  },
  {
    id: '6',
    name: 'Château de Grimaldi',
    ctaName: 'Château de Grimaldi',
    location: 'Aix-en-Provence',
    capacity: '250',
    price: '€14,000 / 3 nights',
    imageUrl: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2000&auto=format&fit=crop',
    description: 'An elegant estate featuring a private chapel and a ruin which serves as a stunning backdrop for outdoor dinners. The property exudes the sophisticated spirit of Aix-en-Provence. With sprawling manicured lawns and a hidden pool area, it offers a variety of picturesque settings for every part of your multi-day wedding celebration.',
    tags: ['Grand Estate', 'Classic'],
    closestAirport: 'Marseille (30 mins)'
  },
  {
    id: '7',
    name: 'Le Mas des Poiriers',
    ctaName: 'Mas des Poiriers',
    location: 'Avignon',
    capacity: '100',
    price: '€35,000 / 7 nights',
    imageUrl: 'https://images.unsplash.com/photo-1507039228507-356617ad36f0?q=80&w=2000&auto=format&fit=crop',
    description: 'The ultimate luxury farmhouse experience, meticulously renovated with high-end finishes and vast pear orchards. It represents the pinnacle of Provencal luxury living. The property is world-renowned for its Pierre Frey interiors and exceptional service standards, offering an exclusive lifestyle experience for the most discerning couples.',
    tags: ['Ultimate Luxury', 'Exclusive'],
    closestAirport: 'Avignon (20 mins)'
  },
  {
    id: '8',
    name: 'Château d\'Estoublon',
    ctaName: 'Château d\'Estoublon',
    location: 'Fontvieille',
    capacity: '200',
    price: '€25,000 / 3 nights',
    imageUrl: 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?q=80&w=2000&auto=format&fit=crop',
    description: 'A world-famous wine and olive oil estate offering a blend of heritage, luxury, and authentic French lifestyle. Set in the heart of the Alpilles, it provides a majestic setting with rows of silver-green olive trees and a grand white-stone facade. The estate\'s own Michelin-standard catering makes it a dream for gourmands.',
    tags: ['Wine & Olives', 'Heritage'],
    closestAirport: 'Marseille (50 mins)'
  },
  {
    id: '9',
    name: 'Villa Kerylos',
    ctaName: 'Villa Kerylos',
    location: 'Beaulieu-sur-Mer',
    capacity: '80',
    price: '€22,000 / 1 night',
    imageUrl: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2000&auto=format&fit=crop',
    description: 'A unique recreation of an Ancient Greek villa, offering unparalleled historical charm on the water\'s edge. Ideal for couples seeking a distinctive and artistic coastal venue. Every mosaic tile and marble pillar tells a story, while the sea-breeze terraces provide a romantic setting for exchange of vows at sunset.',
    tags: ['Historic Charm', 'Seafront'],
    closestAirport: 'Nice (30 mins)'
  },
  {
    id: '10',
    name: 'Grand-Hôtel du Cap-Ferrat',
    ctaName: 'Grand-Hôtel',
    location: 'Cap-Ferrat',
    capacity: '400',
    price: 'On Request',
    imageUrl: 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?q=80&w=2000&auto=format&fit=crop',
    description: 'An icon of the French Riviera, this Four Seasons hotel is the pinnacle of glamour and world-class service. Its manicured lawns and coastal views are legendary. The venue specializes in large-scale luxury events, offering a seamless experience where every detail, from the floral arrangements to the midnight snacks, is executed to perfection.',
    tags: ['Iconic Glamour', 'Resort'],
    closestAirport: 'Nice (35 mins)'
  }
];

export const NAV_LINKS: NavLink[] = [
  { label: 'VENUES', href: '#' },
  { label: 'SERVICES', href: '#' },
  { label: 'REAL WEDDINGS', href: '#' },
  { label: 'BLOG', href: '#' },
  { label: 'CONTACT', href: '#' },
];
