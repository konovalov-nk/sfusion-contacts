import { factory } from 'factory-girl'
import faker from 'faker'
import moment from 'moment'

factory.define('user', Object, {
  firstName: faker.name.firstName(0),
  lastName: faker.name.lastName(0),
  dateOfBirth: moment(faker.date.past()).format('Y-MM-DD')
})

export default factory
