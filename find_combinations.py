#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timedelta

itinerary_min_length = 2
itinerary_max_length = 32
connection_min_delta = timedelta(hours=1)
connection_max_delta = timedelta(hours=4)


class Flight(object):
    """Flight representing class"""
    source = None
    destination = None
    departure = None
    arrival = None
    flight_number = None

    def __init__(self, source, destination, departure, arrival, flight_number):
        self.source = source
        self.destination = destination
        self.departure = datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S')
        self.arrival = datetime.strptime(arrival, '%Y-%m-%dT%H:%M:%S')
        self.flight_number = flight_number

    def __repr__(self):
        return "[%r] %r -> %r @ %r" % (self.flight_number, self.source,
                                       self.destination, self.departure)

    def connects(self, other):
        """Check if other flight can be connected to this one"""
        if self.destination != other.source:
            return False
        stopover_time = other.departure - self.arrival
        if stopover_time < connection_min_delta:
            return False
        if stopover_time > connection_max_delta:
            return False
        return True

    def is_same(self, other):
        """Check if both flights do have the same origin and destination"""
        return self.source == other.source and \
               self.destination == other.destination


class TaskSolver(object):
    """Task solving class"""
    def __init__(self, flight_list):
        self._flights = flight_list
        # sort flights by departure time to optimize searches later
        flight_list.sort(key=lambda o: o.departure)
        self._results = []

    def _find_connections(self, flight_list, flight, itinerary):
        """recursive connection search"""
        itinerary = itinerary[:]  # copy the list, don't append to original
        itinerary.append(flight)
        if len(itinerary) >= itinerary_min_length:
            self._results.append(itinerary)
        if len(itinerary) >= itinerary_max_length:
            return  # avoid unlimited recursion
        for i, f2 in enumerate(flight_list):
            if flight.connects(f2) and not any([f2.is_same(r) for r in itinerary]):
                self._find_connections(flight_list[i + 1:], f2, itinerary)
            elif f2.departure - flight.arrival > connection_max_delta:
                # if this was too late, all following will be late either, prune
                return

    def solve(self):
        for i, f in enumerate(self._flights):
            self._find_connections(flights[i + 1:], f, [])

    def get_results(self):
        return self._results


if __name__ == '__main__':
    input_data = csv.DictReader(iter(sys.stdin.readline, ''))
    # input_data = csv.DictReader(open('input.csv'))
    flights = []
    for row in input_data:
        assert all(key in row for key in ('source', 'destination', 'departure',
                                          'arrival', 'flight_number')), \
                                         'some key missing in input data!'
        f = Flight(**row)
        flights.append(f)

    task_solver = TaskSolver(flights)
    task_solver.solve()

    for r in task_solver.get_results():
        print(','.join([f.flight_number for f in r]))

