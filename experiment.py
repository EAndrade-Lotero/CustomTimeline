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


def get_start_nodes():
    return [
        ChainNode(definition={"dummy": "dummy"})
    ]


class CustomChainTrial(ChainTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):

        return join(
            CodeBlock(
                lambda participant: participant.var.set("round_failed", True)
            ),
            InfoPage(
                "In this page I fail the round.",
                time_estimate=5,
            ),
            InfoPage(
                "I should have skipped this page",
                time_estimate=5,
            ),
            EndRoundPage(
                prompt="This the end-of-round page",
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
            node_class=ChainNode,
            chain_type="within",
            start_nodes=get_start_nodes,
            expected_trials_per_participant=5,
            max_trials_per_participant=5,
            chains_per_participant=1,
            # allow_repeated_nodes=True,
            target_n_participants=60,
            wait_for_networks=True,
            max_nodes_per_chain=2,
            trials_per_node=1,
        ),
    )
