import { useState, useEffect } from 'react';
import { strengthAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Strength = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [strengths, setStrengths] = useState([]);

  useEffect(() => {
    fetchStrengthData();
  }, []);

  const fetchStrengthData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await strengthAPI.getAll();

      const strengthArray = Object.entries(response.data.strengths).map(
        ([currency, data]) => ({ currency, ...data })
      );

      setStrengths(strengthArray.sort((a, b) => a.rank - b.rank));
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load currency strength data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading currency strengths..." />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Currency Strength</h1>
        <button onClick={fetchStrengthData} className="btn-primary">
          Refresh
        </button>
      </div>

      {/* Strength Chart */}
      <Card title="Strength Score Comparison">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={strengths}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="currency" />
            <YAxis domain={[0, 100]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="strength_score" fill="#3b82f6" name="Strength Score" />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      {/* Detailed Strength Table */}
      <Card title="Detailed Currency Analysis">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Rank
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Currency
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Strength Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Momentum
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Trend
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {strengths.map((item) => (
                <tr key={item.currency} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{item.rank}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                    {item.currency}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2" style={{ width: '100px' }}>
                        <div
                          className="bg-primary-600 h-2.5 rounded-full"
                          style={{ width: `${item.strength_score}%` }}
                        ></div>
                      </div>
                      <span className="font-semibold">{item.strength_score.toFixed(2)}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={item.momentum > 0 ? 'text-green-600' : 'text-red-600'}>
                      {item.momentum > 0 ? '+' : ''}{item.momentum.toFixed(2)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      item.trend === 'bullish' ? 'bg-green-100 text-green-800' :
                      item.trend === 'bearish' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {item.trend}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default Strength;
