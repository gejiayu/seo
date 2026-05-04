import { ImageResponse } from 'next/og'

export const runtime = 'edge'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const title = searchParams.get('title')?.slice(0, 60) || 'HouseCar.life'
  const category = searchParams.get('category') || ''
  
  return new ImageResponse(
    (
      <div
        style={{
          height: '100%',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#0f172a',
          backgroundImage: 'linear-gradient(135deg, #0f172a 0%, #1e40af 50%, #3b82f6 100%)',
          padding: '40px',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '30px',
          }}
        >
          <div
            style={{
              fontSize: '48px',
              fontWeight: 'bold',
              color: 'white',
              letterSpacing: '-0.02em',
            }}
          >
            HouseCar.life
          </div>
        </div>
        {category && (
          <div
            style={{
              fontSize: '20px',
              color: '#93c5fd',
              marginBottom: '20px',
              textTransform: 'capitalize',
            }}
          >
            {category.replace(/-/g, ' ')}
          </div>
        )}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            padding: '0 20px',
            maxWidth: '1000px',
          }}
        >
          <div
            style={{
              fontSize: '36px',
              fontWeight: 'bold',
              color: 'white',
              textAlign: 'center',
              lineHeight: 1.3,
            }}
          >
            {title}
          </div>
        </div>
        <div
          style={{
            marginTop: '40px',
            fontSize: '18px',
            color: '#60a5fa',
          }}
        >
          Free Your Business with the Right Tools
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  )
}
