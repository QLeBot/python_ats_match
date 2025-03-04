import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [resume, setResume] = useState('')
  const [matchResults, setMatchResults] = useState(null)
  const [coverLetter, setCoverLetter] = useState('')
  const [optimizedResume, setOptimizedResume] = useState('')
  const [loading, setLoading] = useState(false)

  const handleMatch = async () => {
    try {
      setLoading(true)
      const response = await axios.post('http://localhost:5000/api/match', {
        jobDescription,
        resume
      })
      setMatchResults(response.data)
      setOptimizedResume(response.data.optimized_resume)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateCoverLetter = async () => {
    try {
      setLoading(true)
      const response = await axios.post('http://localhost:5000/api/generate-cover-letter', {
        jobDescription,
        resume
      })
      setCoverLetter(response.data.coverLetter)
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">ATS Matcher</h1>
          
          {/* Job Description Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Job Description</h2>
            <textarea
              className="w-full h-64 p-4 border rounded-lg shadow-sm"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste job description here..."
            />
          </div>

          {/* Resume Section */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Your Resume</h2>
            <textarea
              className="w-full h-64 p-4 border rounded-lg shadow-sm"
              value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder="Paste your resume here..."
            />
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 mb-8">
            <button
              onClick={handleMatch}
              disabled={loading}
              className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
            >
              {loading ? 'Processing...' : 'Analyze Match'}
            </button>
            <button
              onClick={handleGenerateCoverLetter}
              disabled={loading}
              className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600"
            >
              {loading ? 'Generating...' : 'Generate Cover Letter'}
            </button>
          </div>

          {/* Results Section */}
          {matchResults && (
            <div className="space-y-8">
              {/* Match Score */}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-xl font-semibold mb-4">Match Results</h2>
                <div className="text-4xl font-bold text-blue-600">
                  {matchResults.similarity_score}% Match
                </div>
                <div className="mt-4">
                  <h3 className="font-semibold">Matching Keywords:</h3>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {matchResults.matching_keywords.map((keyword, index) => (
                      <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="mt-4">
                  <h3 className="font-semibold">Missing Keywords:</h3>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {matchResults.missing_keywords.map((keyword, index) => (
                      <span key={index} className="bg-red-100 text-red-800 px-3 py-1 rounded-full">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Optimized Resume */}
              {optimizedResume && (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-semibold mb-4">Optimized Resume</h2>
                  <pre className="whitespace-pre-wrap">{optimizedResume}</pre>
                </div>
              )}

              {/* Cover Letter */}
              {coverLetter && (
                <div className="bg-white p-6 rounded-lg shadow">
                  <h2 className="text-xl font-semibold mb-4">Generated Cover Letter</h2>
                  <div className="prose max-w-none">
                    {coverLetter}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
