import { useState, useEffect } from 'react';
import { strengthAPI, insightsAPI, eventsAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { TrendingUp, TrendingDown, Calendar, Target } from 'lucide-react';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState({
    strengths: [],
    insights: [],
    events: [],
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [strengthRes, insightsRes, eventsRes] = await Promise.all([
        strengthAPI.getAll(),
        insightsAPI.getAll(5),
        eventsAPI.getHighImpact(),
      ]);

      const strengthArray = Object.entries(strengthRes.data.strengths).map(
        ([currency, data]) => ({ currency, ...data })
      );

      setData({
        strengths: strengthArray.sort((a, b) => a.rank - b.rank).slice(0, 6),
        insights: insightsRes.data.slice(0, 5),
        events: eventsRes.data.slice(0, 5),
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading dashboard..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={fetchDashboardData}
          className="btn-primary"
        >
          Refresh Data
        </button>
      </div>

      {/* Currency Strength Overview */}
      <Card title="Currency Strength Rankings">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {data.strengths.map((item) => (
            <div
              key={item.currency}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-lg font-bold text-gray-900">{item.currency}</span>
                <span className="text-sm text-gray-500">#{item.rank}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-primary-600">
                  {item.strength_score.toFixed(1)}
                </span>
                <div className={`flex items-center text-sm ${
                  item.trend === 'bullish' ? 'text-green-600' :
                  item.trend === 'bearish' ? 'text-red-600' :
                  'text-gray-600'
                }`}>
                  {item.trend === 'bullish' ? <TrendingUp className="w-4 h-4 mr-1" /> :
                   item.trend === 'bearish' ? <TrendingDown className="w-4 h-4 mr-1" /> : null}
                  {item.trend}
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Top Insights */}
      <Card title="Top Trading Insights">
        <div className="space-y-3">
          {data.insights.map((insight, idx) => (
            <div
              key={idx}
              className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <Target className="w-5 h-5 text-primary-600 mr-2" />
                  <span className="font-semibold text-gray-900">{insight.pair}</span>
                  <span className={`ml-3 px-2 py-1 rounded text-xs font-medium ${
                    insight.signal_type === 'buy' ? 'bg-green-100 text-green-800' :
                    insight.signal_type === 'sell' ? 'bg-red-100 text-red-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {insight.signal_type.toUpperCase()}
                  </span>
                </div>
                <span className="text-sm font-medium text-primary-600">
                  {insight.confidence.toFixed(1)}% confidence
                </span>
              </div>
              <p className="text-sm text-gray-600">{insight.reasoning}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Upcoming High-Impact Events */}
      <Card title="High-Impact Economic Events">
        <div className="space-y-3">
          {data.events.map((event, idx) => (
            <div
              key={idx}
              className="flex items-start border-l-4 border-primary-600 pl-4 py-2"
            >
              <Calendar className="w-5 h-5 text-gray-400 mr-3 mt-0.5" />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-900">{event.event_name}</span>
                  <span className="text-sm text-gray-500">{event.currency}</span>
                </div>
                <div className="text-sm text-gray-600 mt-1">
                  {new Date(event.timestamp).toLocaleString()}
                </div>
                {event.forecast && (
                  <div className="text-xs text-gray-500 mt-1">
                    Forecast: {event.forecast} | Previous: {event.previous || 'N/A'}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
