import { useState } from 'react';
import { pairCompareAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { ArrowRight, TrendingUp, TrendingDown } from 'lucide-react';

const CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD'];

const Compare = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [baseCurrency, setBaseCurrency] = useState('EUR');
  const [quoteCurrency, setQuoteCurrency] = useState('USD');
  const [comparison, setComparison] = useState(null);

  const handleCompare = async () => {
    if (baseCurrency === quoteCurrency) {
      setError('Please select different currencies');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await pairCompareAPI.compare(baseCurrency, quoteCurrency);
      setComparison(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to compare currencies');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Pair Comparison</h1>

      {/* Selection Card */}
      <Card title="Select Currencies to Compare">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Base Currency
            </label>
            <select
              value={baseCurrency}
              onChange={(e) => setBaseCurrency(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              {CURRENCIES.map((curr) => (
                <option key={curr} value={curr}>{curr}</option>
              ))}
            </select>
          </div>

          <ArrowRight className="h-6 w-6 text-gray-400 mt-6" />

          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quote Currency
            </label>
            <select
              value={quoteCurrency}
              onChange={(e) => setQuoteCurrency(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              {CURRENCIES.map((curr) => (
                <option key={curr} value={curr}>{curr}</option>
              ))}
            </select>
          </div>

          <button
            onClick={handleCompare}
            disabled={loading}
            className="btn-primary mt-6"
          >
            {loading ? 'Comparing...' : 'Compare'}
          </button>
        </div>
      </Card>

      {error && <ErrorMessage message={error} />}

      {loading && <LoadingSpinner message="Analyzing pair..." />}

      {/* Comparison Results */}
      {comparison && !loading && (
        <>
          <Card title={`${comparison.pair} Analysis`}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Base Currency */}
              <div className="border border-gray-200 rounded-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {comparison.base_currency.currency} (Base)
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Strength Score:</span>
                    <span className="font-semibold text-lg">
                      {comparison.base_currency.strength.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Momentum:</span>
                    <span className={comparison.base_currency.momentum > 0 ? 'text-green-600' : 'text-red-600'}>
                      {comparison.base_currency.momentum > 0 ? '+' : ''}{comparison.base_currency.momentum.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Trend:</span>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${
                      comparison.base_currency.trend === 'bullish' ? 'bg-green-100 text-green-800' :
                      comparison.base_currency.trend === 'bearish' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {comparison.base_currency.trend}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Global Rank:</span>
                    <span className="font-semibold">#{comparison.base_currency.rank}</span>
                  </div>
                </div>
              </div>

              {/* Quote Currency */}
              <div className="border border-gray-200 rounded-lg p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {comparison.quote_currency.currency} (Quote)
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Strength Score:</span>
                    <span className="font-semibold text-lg">
                      {comparison.quote_currency.strength.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Momentum:</span>
                    <span className={comparison.quote_currency.momentum > 0 ? 'text-green-600' : 'text-red-600'}>
                      {comparison.quote_currency.momentum > 0 ? '+' : ''}{comparison.quote_currency.momentum.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Trend:</span>
                    <span className={`px-2 py-1 rounded text-sm font-medium ${
                      comparison.quote_currency.trend === 'bullish' ? 'bg-green-100 text-green-800' :
                      comparison.quote_currency.trend === 'bearish' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {comparison.quote_currency.trend}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Global Rank:</span>
                    <span className="font-semibold">#{comparison.quote_currency.rank}</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Recommendation */}
          <Card title="Trading Recommendation">
            <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-2xl font-bold text-gray-900">
                  {comparison.recommendation}
                </h3>
                <div className="text-right">
                  <p className="text-sm text-gray-600">Confidence</p>
                  <p className="text-3xl font-bold text-primary-600">
                    {comparison.confidence.toFixed(1)}%
                  </p>
                </div>
              </div>

              <div className="mb-4">
                <p className="text-sm text-gray-600">Strength Divergence</p>
                <div className="flex items-center mt-2">
                  {comparison.divergence > 0 ? (
                    <TrendingUp className="h-6 w-6 text-green-600 mr-2" />
                  ) : (
                    <TrendingDown className="h-6 w-6 text-red-600 mr-2" />
                  )}
                  <span className={`text-2xl font-bold ${
                    comparison.divergence > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {comparison.divergence > 0 ? '+' : ''}{comparison.divergence.toFixed(2)}
                  </span>
                </div>
              </div>

              <div className="border-t border-gray-200 pt-4">
                <p className="text-gray-700">{comparison.analysis}</p>
              </div>
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

export default Compare;
