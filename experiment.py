import psynet.experiment
from psynet.page import InfoPage
from psynet.modular_page import (
    ModularPage, 
    NullControl,
    PushButtonControl,
    ImagePrompt,
    TextControl,
)
from psynet.timeline import (
    Timeline, 
    PageMaker, 
    CodeBlock,
    join,
)
from psynet.trial.chain import (
    ChainTrial,
    ChainTrialMaker,
    ChainNode,
)
from psynet.utils import get_logger

from .custom_timeline import (
    CustomTimeline,
    EndRoundPage,
)

logger = get_logger()
NUM_ROUNDS = 2

def get_start_nodes():
    return [
        CustomChainNode(definition={"dummy": "dummy"})
    ]


class CustomChainNode(ChainNode):

    def create_definition_from_seed(self, seed, experiment, participant):
        return seed

    def summarize_trials(self, trials: list, experiment, participant):
        return {
            "dummy": "dummy"
        }


class CustomChainTrial(ChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        return join(
            CodeBlock(
                lambda participant: participant.var.set("round_failed", True)
            ),
            InfoPage(
                f"In this page I fail the round. (Round {self.position + 1} / {NUM_ROUNDS})",
                time_estimate=5,
            ),
            InfoPage(
                "I should have skipped this page",
                time_estimate=5,
            ),
            EndRoundPage(
                prompt="This is the end-of-round page",
                control=NullControl(),
                save_answer="reward",
                time_estimate=self.time_estimate,
            ),
        )


class Exp(psynet.experiment.Experiment):
    label = "Hello world"

    timeline = CustomTimeline(
        InfoPage(
            "This is the start of the experiment",
            time_estimate=5,
        ),
        ChainTrialMaker(
            id_="custom_chain_trial_maker",
            trial_class=CustomChainTrial,
            node_class=CustomChainNode,
            chain_type="within",
            start_nodes=get_start_nodes,
            expected_trials_per_participant=5,
            max_trials_per_participant=5,
            chains_per_participant=1,
            # allow_repeated_nodes=True,
            target_n_participants=60,
            wait_for_networks=True,
            max_nodes_per_chain=NUM_ROUNDS,
            trials_per_node=1,
        ),
    )
