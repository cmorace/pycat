"""The Publisher module implements the Publisher class and Subscriber Type"""

from typing import Callable, Generic, TypeVar, Union, Set, List

Subscriber = TypeVar('Subscriber', bound=Callable)


class Publisher(Generic[Subscriber]):
    """The Publisher class dispatches events to a set of subscribers.

    The class maintains a set of callable Subscribers.
    The Subscriber type is generic and must be specified when
    instantiating the Publisher class.

    :param Generic: the Callable type or Protocol
    of the Subscribers functions
    :type Generic: TypeVar('Subscriber', bound=Callable)
    """
    def __init__(self):
        """Instantiate a new Publisher object.

        Requires a template argument for the type of subscriber
        e.g. `subject = Subject[Callable[[int], None]]()'
        """
        self._current_subscribers: Set[Subscriber] = set()
        self._new_subscribers: Set[Subscriber] = set()

    def add_subscribers(self, subscribers: Union[Subscriber,
                                                 List[Subscriber]]):
        """Add a subscriber or list of subscribers called by `dispatch()`.

        User's of this function are responsible for removing the
        subscribers when the objects being dispatched no longer require
        event updates. If the subscribers are not removed the objects will
        not be garbage collected.
        To remove the subscribers use `remove_subscribers()`

        :param subscribers: a single subscriber or a list of subscribers
        :type subscribers: Union[Subscriber, List[Subscriber]]
        """
        if isinstance(subscribers, list):
            for subscriber in subscribers:
                self._new_subscribers.add(subscriber)
        else:
            self._new_subscribers.add(subscribers)

    def remove_subscribers(self, subscribers: Union[Subscriber,
                                                    List[Subscriber]]):
        """Remove a subscriber or list o subscribers.

        :param subscribers: a single subscriber or a list of subscribers
        :type subscribers: Union[Subscribers, List[Subscribers]]
        """
        if isinstance(subscribers, list):
            for subscriber in subscribers:
                self._new_subscribers.remove(subscriber)
        else:
            self._new_subscribers.remove(subscribers)

    def publish(self, *args):
        """Call all of the current subscribers.

        Be careful not to update current subscribers during dispatch
        """
        for subscriber in self._current_subscribers:
            subscriber(*args)

    def update(self):
        """Update the current subscribers.

        Be careful not to update current subscribers during dispatch
        """
        if self._current_subscribers != self._new_subscribers:
            self._current_subscribers = set(self._new_subscribers)
