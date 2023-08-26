from db_work.crud.implemented import event_service


class AdminRequest:
    def get_events(self):
        return event_service.get_all_events()

    def create_event(self, event_data):
        return event_service.create_event(event_data)

    def update_event(self, event_id, update_data):
        event = event_service.get_event_by_bid(event_id)
        if event:
            event_service.update_event(event, update_data)

    def delete_event(self, event_id):
        event = event_service.get_event_by_bid(event_id)
        if event:
            event_service.delete_event(event)
