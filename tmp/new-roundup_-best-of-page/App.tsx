import React from 'react';
import VenueCard from './components/VenueCard';
import { VENUES } from './constants';
import { Venue } from './types';

const App: React.FC = () => {
  // Helper to find venue by name for the featured sections
  const findVenue = (name: string): Venue | undefined => {
    return VENUES.find(v => v.name.toLowerCase().includes(name.toLowerCase()));
  };

  return (
    <div className="min-h-screen bg-white selection:bg-fws-green selection:text-white pb-16">
      {/* Blog Post Content Area */}
      <main className="max-w-6xl mx-auto px-4 md:px-8">
        
        {/* Article Header */}
        <header className="py-16 text-center border-b border-fws-green/10 mb-12">
          <h1 className="text-5xl md:text-7xl lg:text-8xl mb-6 max-w-5xl mx-auto">
            Wedding Venues in the South of France
          </h1>
          
          <p className="text-lg md:text-xl font-serif text-fws-grey italic max-w-3xl mx-auto leading-relaxed">
            From the rolling hills of Provence to the glitz of the French Riviera, discover our handpicked selection of the most exquisite estates for your dream French wedding.
          </p>
        </header>

        {/* Intro Text */}
        <div className="max-w-4xl mx-auto text-base text-fws-grey font-light leading-relaxed mb-8 space-y-4">
          <p>
            The South of France is more than just a destination; it's a feeling. It's the scent of lavender on a warm breeze, the rhythmic song of cicadas, and the sparkle of the Mediterranean sun on ancient stone walls. Planning a wedding in this corner of the world means choosing a backdrop of unparalleled beauty and timeless romance.
          </p>
          <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark pt-8 pb-4">Our Top 10 South of France Venue Comparison</h2>
          <p>
            To help you navigate through the finest options available, we have compiled a quick-reference table of our favorite venues across the region. Use this to filter by your primary needs—whether that's guest capacity or an approximate starting price point.
          </p>
        </div>

        {/* Comparison Table */}
        <div className="mb-8 max-w-5xl mx-auto">
          <div className="overflow-x-auto border border-fws-green/20 shadow-md relative rounded-xl overflow-hidden">
            <table className="w-full text-left border-collapse min-w-[700px]">
              <thead>
                <tr className="bg-fws-light border-b border-fws-green/30">
                  <th className="sticky left-0 z-20 bg-fws-light py-3 px-5 text-[9px] font-bold tracking-[0.2em] text-fws-dark uppercase border-r border-fws-green/10">Venue Name</th>
                  <th className="py-3 px-5 text-[9px] font-bold tracking-[0.2em] text-fws-dark uppercase">Best For</th>
                  <th className="py-3 px-5 text-[9px] font-bold tracking-[0.2em] text-fws-dark uppercase">Region</th>
                  <th className="py-3 px-5 text-[9px] font-bold tracking-[0.2em] text-fws-dark uppercase">From Price</th>
                  <th className="py-3 px-5 text-[9px] font-bold tracking-[0.2em] text-fws-dark uppercase">Capacity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-fws-green/10">
                {VENUES.map((venue) => (
                  <tr key={venue.id} className="hover:bg-fws-light/50 transition-colors">
                    <td className="sticky left-0 z-10 bg-white py-2 px-1 text-xs font-sans font-bold text-fws-dark border-r border-fws-green/10 whitespace-nowrap">
                      <a href={`#${venue.id}`} className="hover:text-fws-green transition-colors duration-300">
                        {venue.name}
                      </a>
                    </td>
                    <td className="py-2 px-5 text-xs font-medium text-fws-grey font-sans tracking-tight">
                      {venue.tags[0]}
                    </td>
                    <td className="py-2 px-5 text-xs text-fws-grey font-medium font-sans">
                      {venue.location}
                    </td>
                    <td className="py-2 px-5 text-xs font-bold text-fws-green font-sans whitespace-nowrap">
                      {venue.price}
                    </td>
                    <td className="py-2 px-5 text-xs text-fws-grey font-medium font-sans">
                      {venue.capacity} guests
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-[9px] text-fws-grey italic text-center uppercase tracking-widest opacity-60">Scroll horizontally to view all columns on mobile</p>
        </div>

        {/* Key Insights Section - Larger text, reduced white space */}
        <div className="max-w-5xl mx-auto mb-16">
          <div className="bg-fws-light/60 border border-fws-green/10 p-8 rounded-xl shadow-sm">
            <h3 className="text-[13px] tracking-[0.3em] font-bold text-fws-green uppercase mb-4 flex items-center gap-3">
              <span className="w-12 h-px bg-fws-green/30"></span>
              Key Insights & Expert Takeaways
              <span className="w-12 h-px bg-fws-green/30"></span>
            </h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="space-y-1.5">
                <h4 className="font-serif text-fws-dark text-xl italic border-b border-fws-green/10 pb-1">Accessibility</h4>
                <p className="text-base text-fws-grey leading-relaxed font-light">
                  Most premier estates are within a 45-minute drive of major hubs like <span className="text-fws-dark font-medium">Marseille (MRS)</span> or <span className="text-fws-dark font-medium">Nice (NCE)</span>.
                </p>
              </div>
              <div className="space-y-1.5">
                <h4 className="font-serif text-fws-dark text-xl italic border-b border-fws-green/10 pb-1">Optimal Timing</h4>
                <p className="text-base text-fws-grey leading-relaxed font-light">
                  <span className="text-fws-dark font-medium">June and September</span> are the prime months for perfect light and manageable temperatures.
                </p>
              </div>
              <div className="space-y-1.5">
                <h4 className="font-serif text-fws-dark text-xl italic border-b border-fws-green/10 pb-1">Budgeting</h4>
                <p className="text-base text-fws-grey leading-relaxed font-light">
                  Venue hire often includes exclusive use for <span className="text-fws-dark font-medium">3 days</span>, allowing for a relaxed arrival and recovery.
                </p>
              </div>
              <div className="space-y-1.5">
                <h4 className="font-serif text-fws-dark text-xl italic border-b border-fws-green/10 pb-1">Legal Facts</h4>
                <p className="text-base text-fws-grey leading-relaxed font-light">
                  Foreign couples typically marry civilly in their home country, hosting a <span className="text-fws-dark font-medium">symbolic blessing</span> in France.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Detailed Informational Content */}
        <div className="max-w-4xl mx-auto mb-16 space-y-16">
          
          <section>
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-4">Why Choose the South of France for Your Wedding?</h2>
            <p className="text-fws-grey font-light leading-relaxed text-base">
              If you still need convincing, let us paint the picture. From the rolling lavender fields of the Luberon to the dramatic limestone peaks of Les Alpilles, the landscapes are as diverse as they are accessible. Located just one hour from Marseille Provence Airport or the gateway of Nice Côte d’Azur, the region offers a Mediterranean climate with long, sun-drenched summers that make outdoor "al fresco" dining under the stars a reality.
            </p>
          </section>

          {/* Destinations Section */}
          <section id="destinations">
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-8">What Are the Best Wedding Destinations in the South of France?</h2>
            
            <div className="space-y-12">
              <div className="border-l-2 border-fws-green/20 pl-8">
                <h3 className="text-2xl text-fws-dark mb-3">The Luberon & Gordes</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8">
                  Known as the cultural heart of Provence, the Luberon is a tapestry of vineyards, olive groves, and ancient hilltop villages. Gordes, a majestic stone village perched on a cliff, offers some of the most romantic sunsets in France, making it a premier choice for those seeking refined, pastoral elegance.
                </p>
                {findVenue('Le Mas des Poiriers') && <VenueCard venue={findVenue('Le Mas des Poiriers')!} index={0} />}
                <div className="mt-16">
                  {findVenue('Château de la Croix') && <VenueCard venue={findVenue('Château de la Croix')!} index={1} />}
                </div>
              </div>

              <div className="border-l-2 border-fws-green/20 pl-8">
                <h3 className="text-2xl text-fws-dark mb-3">Les Alpilles & Aix-en-Provence</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8">
                  Characterized by its rugged white limestone peaks and silver-green landscape, Les Alpilles is home to Saint-Rémy-de-Provence and some of the region's most historic wine estates. This area offers a chic, low-key luxury that is deeply rooted in local traditions.
                </p>
                {findVenue('Estoublon') && <VenueCard venue={findVenue('Estoublon')!} index={2} />}
                <div className="mt-16">
                  {findVenue('Grimaldi') && <VenueCard venue={findVenue('Grimaldi')!} index={3} />}
                </div>
              </div>

              <div className="border-l-2 border-fws-green/20 pl-8">
                <h3 className="text-2xl text-fws-dark mb-3">Côte d'Azur (French Riviera)</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8">
                  The French Riviera is synonymous with mythic glamour and high-end coastal living. From the grand palaces of Cap-Ferrat to the artistic villas of Beaulieu-sur-Mer, this stretch of coastline offers unmatched azure views and an international atmosphere.
                </p>
                <div className="space-y-16">
                  {findVenue('Ephrussi') && <VenueCard venue={findVenue('Ephrussi')!} index={4} />}
                  {findVenue('Grand-Hôtel du Cap-Ferrat') && <VenueCard venue={findVenue('Grand-Hôtel du Cap-Ferrat')!} index={5} />}
                  {findVenue('Kerylos') && <VenueCard venue={findVenue('Kerylos')!} index={6} />}
                </div>
              </div>
            </div>
          </section>

          {/* Types Section */}
          <section id="types">
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-8">What Types of Wedding Venues Can You Find in the South of France?</h2>
            
            <div className="space-y-16">
              <div>
                <h3 className="text-2xl text-fws-green mb-4">Fairytale Chateaux</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8 max-w-3xl">
                  For the ultimate romantic experience, the South of France boasts an array of fairytale chateaux. These historic monuments have been carefully restored to offer modern luxury while retaining their original turrets, private chapels, and grand ballrooms.
                </p>
                <div className="space-y-16">
                  {findVenue('Robernier') && <VenueCard venue={findVenue('Robernier')!} index={7} />}
                </div>
              </div>

              <div>
                <h3 className="text-2xl text-fws-green mb-4">Authentic Bastides & Mas</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8 max-w-3xl">
                  A "Mas" or "Bastide" offers an intimate and earthy luxury. These traditional stone farmhouses and manor houses are perfect for long, family-style dinners under the shade of plane trees.
                </p>
                {findVenue('Saint-Mathieu') && <VenueCard venue={findVenue('Saint-Mathieu')!} index={8} />}
              </div>

              <div>
                <h3 className="text-2xl text-fws-green mb-4">Coastal & Cliffside</h3>
                <p className="text-fws-grey text-base font-light leading-relaxed mb-8 max-w-3xl">
                  Embrace the sea with venues that cling to the dramatic cliffs of the Calanques or sit right on the water's edge.
                </p>
                {findVenue('Canaille') && <VenueCard venue={findVenue('Canaille')!} index={9} />}
              </div>
            </div>
          </section>

          {/* Expanded Cost Section */}
          <section id="cost" className="bg-fws-light p-10 md:p-14 border-y border-fws-green/10">
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-8 text-center">The Real Cost of a South of France Wedding</h2>
            
            <div className="max-w-3xl mx-auto text-base text-fws-grey font-light leading-relaxed mb-12 text-center">
              <p>
                While the region is known for luxury, the cost of a wedding varies significantly based on your "Big Three": Venue, Catering, and Accommodation. Below is a detailed breakdown of what to expect for a standard 100-guest wedding in high season.
              </p>
            </div>

            {/* Price Category Grid */}
            <div className="grid md:grid-cols-3 gap-8 mb-16">
              <div className="bg-white p-6 rounded-lg shadow-sm border-t-4 border-fws-green/30">
                <h4 className="text-fws-green font-bold text-[10px] uppercase tracking-[0.2em] mb-4">The "Chic Boutique"</h4>
                <div className="space-y-4">
                  <div>
                    <p className="text-fws-dark font-serif text-lg leading-tight">€15k - €30k Total</p>
                    <p className="text-[10px] text-fws-grey italic">Ideal for: Bastides & Intimate Mas</p>
                  </div>
                  <ul className="text-xs text-fws-grey space-y-2 list-disc pl-4 font-sans">
                    <li>Venue Hire: €5k - €10k / 2 nights</li>
                    <li>Catering: €150 - €180 per head</li>
                    <li>Simple local florals & DIY decor</li>
                    <li>Local DJ & Acoustic Duo</li>
                  </ul>
                </div>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-md border-t-4 border-fws-green relative scale-105 z-10">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-fws-green text-white text-[8px] font-bold px-4 py-1.5 rounded-full uppercase tracking-widest">Most Popular</div>
                <h4 className="text-fws-green font-bold text-[10px] uppercase tracking-[0.2em] mb-4">The "Heritage Grandeur"</h4>
                <div className="space-y-4">
                  <div>
                    <p className="text-fws-dark font-serif text-xl leading-tight">€45k - €75k Total</p>
                    <p className="text-[10px] text-fws-grey italic">Ideal for: Classic Chateaux</p>
                  </div>
                  <ul className="text-xs text-fws-grey space-y-2 list-disc pl-4 font-sans">
                    <li>Venue Hire: €12k - €20k / 3 nights</li>
                    <li>Catering: €200 - €250 per head</li>
                    <li>Full planning service included</li>
                    <li>Multi-day events (Brunch etc)</li>
                  </ul>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border-t-4 border-fws-green/30">
                <h4 className="text-fws-green font-bold text-[10px] uppercase tracking-[0.2em] mb-4">The "Ultra Luxe"</h4>
                <div className="space-y-4">
                  <div>
                    <p className="text-fws-dark font-serif text-lg leading-tight">€100k+ Total</p>
                    <p className="text-[10px] text-fws-grey italic">Ideal for: Cap-Ferrat Palaces</p>
                  </div>
                  <ul className="text-xs text-fws-grey space-y-2 list-disc pl-4 font-sans">
                    <li>Venue Buyouts: €35k+ / 3 nights</li>
                    <li>Michelin-standard catering</li>
                    <li>High-end production & lighting</li>
                    <li>Guest concierge services</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Hidden Costs & Seasonal Grid */}
            <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-12 pt-10 border-t border-fws-green/10">
              <div>
                <h3 className="text-fws-dark text-2xl mb-4">Common "Hidden" Expenses</h3>
                <ul className="space-y-3">
                  <li className="flex items-start gap-3">
                    <svg className="w-4 h-4 text-fws-green mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="text-sm text-fws-grey leading-relaxed"><span className="text-fws-dark font-bold">SACEM Tax:</span> The French music rights fee. Often around €150-€300 depending on guest count and music type.</p>
                  </li>
                  <li className="flex items-start gap-3">
                    <svg className="w-4 h-4 text-fws-green mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="text-sm text-fws-grey leading-relaxed"><span className="text-fws-dark font-bold">Security & Cleaning:</span> Historic chateaux often require a mandatory security guard and professional cleaning crew fee (€500-€1,200).</p>
                  </li>
                  <li className="flex items-start gap-3">
                    <svg className="w-4 h-4 text-fws-green mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <p className="text-sm text-fws-grey leading-relaxed"><span className="text-fws-dark font-bold">Electricity Surcharge:</span> If you are bringing in heavy production (stage lighting, sound), some older estates charge for power consumption.</p>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="text-fws-dark text-2xl mb-4">Seasonal Savings</h3>
                <p className="text-sm text-fws-grey leading-relaxed mb-4 font-light">
                  To maximize your budget, consider the <span className="text-fws-green font-bold italic">"Shoulder Seasons"</span>. 
                </p>
                <div className="space-y-4">
                  <div className="flex justify-between items-center text-[10px] font-bold tracking-widest uppercase border-b border-fws-green/10 pb-2">
                    <span className="text-fws-dark">High Season (July - Aug)</span>
                    <span className="text-fws-green">100% Price</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-bold tracking-widest uppercase border-b border-fws-green/10 pb-2">
                    <span className="text-fws-dark">Mid Season (June / Sept)</span>
                    <span className="text-fws-green">85% - 90% Price</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] font-bold tracking-widest uppercase border-b border-fws-green/10 pb-2">
                    <span className="text-fws-dark">Low Season (Oct - May)</span>
                    <span className="text-fws-green">60% - 75% Price</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Expert Tips Section */}
          <section id="expert-tips">
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-8">Expert Tips for Your Paris Wedding</h2>
            <div className="grid md:grid-cols-2 gap-x-12 gap-y-12">
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-full bg-fws-green/10 text-fws-green flex items-center justify-center font-bold text-xs">1</span>
                  <h4 className="text-base font-bold text-fws-dark">The "Sunrise" Portrait Session</h4>
                </div>
                <p className="text-sm text-fws-grey font-light leading-relaxed">
                  To get those iconic, empty shots at the Louvre or Trocadéro, you must shoot at sunrise.
                </p>
              </div>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-full bg-fws-green/10 text-fws-green flex items-center justify-center font-bold text-xs">2</span>
                  <h4 className="text-base font-bold text-fws-dark">Think Vertically for Views</h4>
                </div>
                <p className="text-sm text-fws-grey font-light leading-relaxed">
                  Many of the best Eiffel Tower views are from private terraces.
                </p>
              </div>
            </div>
          </section>

          {/* BRIDE'S TIP BLOCK */}
          <div className="max-w-4xl mx-auto my-12">
            <div className="bg-fws-light/40 border-2 border-fws-green/10 p-8 md:p-12 rounded-lg relative text-center">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-white px-6 py-1 border border-fws-green/30 rounded-full shadow-sm flex items-center gap-3">
                <svg className="w-4 h-4 text-fws-green" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
                <span className="text-[10px] font-bold tracking-[0.3em] text-fws-green uppercase">Bride's Tip</span>
              </div>
              <h3 className="text-2xl md:text-3xl text-fws-dark mb-6 mt-4">The "Secret" Parisian Golden Hour</h3>
              <p className="text-base md:text-lg text-fws-grey italic font-serif leading-relaxed max-w-2xl mx-auto">
                "If you are planning an outdoor ceremony in a Parisian garden, aim for an early evening start. The light reflects off the limestone buildings in a way that turns the city a soft, powdery pink."
              </p>
            </div>
          </div>

          {/* FAQ Section */}
          <section id="faq" className="border-t border-fws-green/20 pt-16">
            <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-12 text-center italic">Comprehensive FAQ</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">Can foreigners legally marry in France?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  Legally, one partner must reside in the town for at least 40 days prior to the wedding. Consequently, 99% of destination couples choose to have a simple civil ceremony in their home country and then host a stunning "Symbolic Ceremony" or religious blessing in France.
                </p>
              </div>
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">What is a "Plan B" and do I need one?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  Even in the sunny South, rain can happen. A proper "Plan B" is an indoor space or high-quality marquee that can fit your entire guest list for both the ceremony and dinner. Never book a venue that doesn't have a backup space you genuinely love.
                </p>
              </div>
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">Do venues have noise curfews?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  Yes. Many venues located near villages have a 2 AM music limit. If you plan to party until sunrise, look for isolated "Mas" or larger private estates like Château de Robernier which are more flexible with late-night celebrations.
                </p>
              </div>
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">How much should I budget per guest?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  For mid-to-high-end weddings in this region, expect a total investment of €1,500–€2,500 per guest. This typically covers the venue, premium catering, open bar, florals, photography, and the full multi-day event experience.
                </p>
              </div>
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">Is it easy for guests to travel here?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  Extremely. Marseille (MRS) and Nice (NCE) airports serve most major international hubs. The high-speed TGV train also connects Paris to Avignon or Aix-en-Provence in under 3 hours, making it very accessible for guests coming from the capital.
                </p>
              </div>
              <div className="bg-fws-light p-8 rounded-lg shadow-sm">
                <h4 className="text-sm font-bold text-fws-dark mb-3">Should I hire a local wedding planner?</h4>
                <p className="text-sm text-fws-grey font-light leading-relaxed italic">
                  Unless you speak fluent French and have significant experience in event production, yes. A local planner will have established relationships with vendors, understand local contracts, and manage the complex logistics of a destination wedding.
                </p>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default App;