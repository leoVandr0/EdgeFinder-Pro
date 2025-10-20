import { useState, useEffect } from 'react';
import { insightsAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { Target, TrendingUp, TrendingDown } from 'lucide-react';

const Insights = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [insights, setInsights] = useState([]);
  const [limit, setLimit] = useState(10);

  useEffect(() => {
    fetchInsights();
  }, [limit]);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await insightsAPI.getAll(limit);
      setInsights(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  const getSignalColor = (type) => {
    return type === 'buy' ? 'text-green-600' : type === 'sell' ? 'text-red-600' : 'text-gray-600';
  };

  const getSignalBg = (type) => {
    return type === 'buy' ? 'bg-green-100' : type === 'sell' ? 'bg-red-100' : 'bg-gray-100';
  };

  if (loading) return <LoadingSpinner message="Loading insights..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Trading Insights</h1>
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-600">Show:</label>
          <select
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          >
            <option value={5}>5 insights</option>
            <option value={10}>10 insights</option>
            <option value={20}>20 insights</option>
            <option value={50}>50 insights</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {insights.map((insight, idx) => (
          <Card key={idx} className="hover:shadow-lg transition-shadow">
            <div className="space-y-4">
              {/* Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Target className="h-6 w-6 text-primary-600 mr-3" />
                  <h3 className="text-2xl font-bold text-gray-900">{insight.pair}</h3>
                </div>
                <span className={`px-3 py-1 rounded-lg text-sm font-bold ${getSignalBg(insight.signal_type)} ${getSignalColor(insight.signal_type)}`}>
                  {insight.signal_type.toUpperCase()}
                </span>
              </div>

              {/* Confidence Bar */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Confidence</span>
                  <span className="text-lg font-bold text-primary-600">
                    {insight.confidence.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-primary-600 h-3 rounded-full transition-all"
                    style={{ width: `${insight.confidence}%` }}
                  ></div>
                </div>
              </div>

              {/* Price Levels */}
              <div className="grid grid-cols-3 gap-4 pt-3 border-t border-gray-200">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Entry</p>
                  <p className="font-semibold text-gray-900">{insight.entry_price.toFixed(4)}</p>
                </div>
                <div>
                  <p className="text-xs text-red-600 mb-1">Stop Loss</p>
                  <p className="font-semibold text-red-600">{insight.stop_loss.toFixed(4)}</p>
                </div>
                <div>
                  <p className="text-xs text-green-600 mb-1">Take Profit</p>
                  <p className="font-semibold text-green-600">{insight.take_profit.toFixed(4)}</p>
                </div>
              </div>

              {/* Risk/Reward */}
              <div className="flex items-center justify-between text-sm pt-2 border-t border-gray-200">
                <span className="text-gray-600">Timeframe:</span>
                <span className="font-semibold text-gray-900">{insight.timeframe}</span>
              </div>

              {/* Reasoning */}
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-700">{insight.reasoning}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Insights;
