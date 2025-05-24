import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ArrowRight, Video, Mic, Sparkles } from "lucide-react"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent mb-6">
              VIDUS AI
            </h1>
            <p className="text-2xl text-muted-foreground mb-4">Advanced Video & Audio Dubbing Platform</p>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
              Transform your content with cutting-edge voice cloning and dubbing technology. Upload your videos or audio
              files and let AI create perfect voice matches.
            </p>

            <Link href="/upload">
              <Button size="lg" className="text-lg px-8 py-6 rounded-xl shadow-lg hover:shadow-xl transition-all">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <Card className="border-2 hover:border-primary/50 transition-colors">
              <CardContent className="pt-6 text-center">
                <Video className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Video Dubbing</h3>
                <p className="text-muted-foreground">
                  Replace audio in videos with AI-generated voices that match perfectly
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary/50 transition-colors">
              <CardContent className="pt-6 text-center">
                <Mic className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Voice Cloning</h3>
                <p className="text-muted-foreground">
                  Create realistic voice clones from audio samples with advanced AI
                </p>
              </CardContent>
            </Card>

            <Card className="border-2 hover:border-primary/50 transition-colors">
              <CardContent className="pt-6 text-center">
                <Sparkles className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">AI Enhancement</h3>
                <p className="text-muted-foreground">Enhance audio quality and remove background noise automatically</p>
              </CardContent>
            </Card>
          </div>

          {/* CTA Section */}
          <Card className="bg-gradient-to-r from-primary/10 to-primary/5 border-primary/20">
            <CardContent className="pt-8 pb-8">
              <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Content?</h2>
              <p className="text-lg text-muted-foreground mb-6">
                Upload your video or audio files and experience the power of AI-driven voice technology
              </p>
              <Link href="/upload">
                <Button size="lg" className="text-lg px-8 py-4">
                  Start Processing Now
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
