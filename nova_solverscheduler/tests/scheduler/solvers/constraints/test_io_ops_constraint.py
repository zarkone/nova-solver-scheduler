# Copyright (c) 2014 Cisco Systems, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from nova import test
from nova_solverscheduler.scheduler.solvers.constraints \
        import io_ops_constraint
from nova_solverscheduler.tests.scheduler import solver_scheduler_fakes \
        as fakes


class TestIoOpsConstraint(test.NoDBTestCase):

    def setUp(self):
        super(TestIoOpsConstraint, self).setUp()
        self.constraint_cls = io_ops_constraint.IoOpsConstraint
        self._generate_fake_constraint_input()

    def _generate_fake_constraint_input(self):
        self.fake_filter_properties = {
                'instance_uuids': ['fake_uuid_%s' % x for x in range(2)],
                'num_instances': 2}
        host1 = fakes.FakeSolverSchedulerHostState('host1', 'node1',
                {'num_io_ops': 6})
        host2 = fakes.FakeSolverSchedulerHostState('host2', 'node1',
                {'num_io_ops': 10})
        host3 = fakes.FakeSolverSchedulerHostState('host3', 'node1',
                {'num_io_ops': 15})
        self.fake_hosts = [host1, host2, host3]

    def test_get_constraint_matrix(self):
        self.flags(max_io_ops_per_host=7)
        expected_cons_mat = [
            [True, False],
            [False, False],
            [False, False]]
        cons_mat = self.constraint_cls().get_constraint_matrix(
                    self.fake_hosts, self.fake_filter_properties)
        self.assertEqual(expected_cons_mat, cons_mat)

    def test_get_constraint_matrix2(self):
        self.flags(max_io_ops_per_host=15)
        expected_cons_mat = [
            [True, True],
            [True, True],
            [False, False]]
        cons_mat = self.constraint_cls().get_constraint_matrix(
                    self.fake_hosts, self.fake_filter_properties)
        self.assertEqual(expected_cons_mat, cons_mat)
