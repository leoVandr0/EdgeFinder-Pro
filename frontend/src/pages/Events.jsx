import { useState, useEffect } from 'react';
import { eventsAPI } from '../api/api';
import Card from '../components/Card';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { Calendar, AlertCircle } from 'lucide-react';

const Events = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [events, setEvents] = useState([]);
  const [filter, setFilter] = useState('upcoming');

  useEffect(() => {
    fetchEvents();
  }, [filter]);

  const fetchEvents = async () => {
    try {
      setLoading(true);
      setError(null);

      let response;
      if (filter === 'today') {
        response = await eventsAPI.getToday();
      } else if (filter === 'high-impact') {
        response = await eventsAPI.getHighImpact();
      } else {
        response = await eventsAPI.getAll({ upcoming: filter === 'upcoming' });
      }

      setEvents(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load events');
    } finally {
      setLoading(false);
    }
  };

  const getImpactBadge = (impact) => {
    const colors = {
      High: 'bg-red-100 text-red-800',
      Medium: 'bg-yellow-100 text-yellow-800',
      Low: 'bg-green-100 text-green-800',
    };
    return colors[impact] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Economic Calendar</h1>
        <div className="flex space-x-2">
          <button
            onClick={() => setFilter('upcoming')}
            className={filter === 'upcoming' ? 'btn-primary' : 'btn-secondary'}
          >
            Upcoming
          </button>
          <button
            onClick={() => setFilter('today')}
            className={filter === 'today' ? 'btn-primary' : 'btn-secondary'}
          >
            Today
          </button>
          <button
            onClick={() => setFilter('high-impact')}
            className={filter === 'high-impact' ? 'btn-primary' : 'btn-secondary'}
          >
            High Impact
          </button>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner message="Loading events..." />
      ) : error ? (
        <ErrorMessage message={error} />
      ) : events.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <Calendar className="mx-auto h-12 w-12 text-gray-400" />
            <p className="mt-4 text-gray-600">No events found for the selected filter</p>
          </div>
        </Card>
      ) : (
        <Card title={`${events.length} Events`}>
          <div className="space-y-4">
            {events.map((event, idx) => (
              <div
                key={idx}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="font-bold text-gray-900">{event.currency}</span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getImpactBadge(event.impact)}`}>
                        {event.impact} Impact
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {event.event_name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {new Date(event.timestamp).toLocaleString('en-US', {
                        weekday: 'short',
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </p>
                  </div>
                  {event.impact === 'High' && (
                    <AlertCircle className="h-6 w-6 text-red-600" />
                  )}
                </div>

                {(event.actual || event.forecast || event.previous) && (
                  <div className="mt-3 grid grid-cols-3 gap-4 pt-3 border-t border-gray-200">
                    {event.actual && (
                      <div>
                        <p className="text-xs text-gray-500">Actual</p>
                        <p className="font-semibold text-gray-900">{event.actual}</p>
                      </div>
                    )}
                    {event.forecast && (
                      <div>
                        <p className="text-xs text-gray-500">Forecast</p>
                        <p className="font-semibold text-gray-900">{event.forecast}</p>
                      </div>
                    )}
                    {event.previous && (
                      <div>
                        <p className="text-xs text-gray-500">Previous</p>
                        <p className="font-semibold text-gray-900">{event.previous}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};

export default Events;
